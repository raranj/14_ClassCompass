from collections import defaultdict
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from .models import AIRequestLog

COMPUTE_RATE_PER_HOUR = 0.07

INPUT_LABELS = {
    "pdf": "PDF",
    "docx": "DOCX",
    "html": "HTML",
    "text": "Pasted Text",
}

def estimated_cost(seconds):
    return seconds/3600*COMPUTE_RATE_PER_HOUR

@login_required
def analytics_dashboard(request):
    logs = list(
        AIRequestLog.objects.filter(
            user=request.user
        ).order_by("created_at")
    )
    total_requests = len(logs)
    total_latency = sum(
        log.latency_seconds for log in logs
    )
    total_tokens = sum(
        log.generated_tokens for log in logs
    )
    total_extracted = sum(
        log.extracted_events for log in logs
    )
    total_saved = sum(
        log.saved_events for log in logs
    )
    average_latency = (
        total_latency/total_requests
        if total_requests else 0
    )
    average_tokens = (
        total_tokens/total_requests
        if total_requests else 0
    )
    average_cost = (
        estimated_cost(total_latency)/total_requests
        if total_requests else 0
    )
    total_cost = estimated_cost(total_latency)
    save_rate = (
        total_saved/total_extracted*100
        if total_extracted else 0
    )
    scatter_points = [
        {
            "x": log.syllabus_length,
            "y": round(log.latency_seconds, 3),
        }
        for log in logs
        if log.syllabus_length > 0
    ]
    method_counts = {
        key: 0 for key in INPUT_LABELS
    }
    method_tokens = {
        key: [] for key in INPUT_LABELS
    }
    for log in logs:
        method_counts[log.input_method] = (
            method_counts.get(log.input_method, 0) + 1
        )
        method_tokens.setdefault(
            log.input_method, []
        ).append(log.generated_tokens)
    average_tokens_by_method = {
        key: (
            sum(method_tokens[key])/len(method_tokens[key])
            if method_tokens[key] else 0
        )
        for key in INPUT_LABELS
    }
    daily = defaultdict(lambda: {
        "count": 0,
        "latency": 0.0,
        "cost": 0.0,
    })
    for log in logs:
        day = timezone.localtime(
            log.created_at
        ).date().isoformat()
        daily[day]["count"] += 1
        daily[day]["latency"] += log.latency_seconds
        daily[day]["cost"] += estimated_cost(
            log.latency_seconds
        )
    if daily:
        start_date = min(
            timezone.datetime.fromisoformat(day).date()
            for day in daily
        )
        end_date = timezone.localdate()
        start_date = max(
            start_date,
            end_date - timedelta(days=89)
        )
        day_labels = []
        current_day = start_date
        while current_day <= end_date:
            day_labels.append(current_day.isoformat())
            current_day += timedelta(days=1)
    else:
        day_labels = []
    daily_counts = [
        daily[day]["count"]
        for day in day_labels
    ]
    daily_average_latency = [
        (
            round(
                daily[day]["latency"] /
                daily[day]["count"], 2
            )
            if daily[day]["count"] else None
        )
        for day in day_labels
    ]
    cumulative_cost = []
    running_cost = sum(
        log.latency_seconds/3600
       *COMPUTE_RATE_PER_HOUR
        for log in logs
        if (
            day_labels
            and timezone.localtime(log.created_at)
                .date().isoformat() < day_labels[0]
        )
    )
    for day in day_labels:
        running_cost += daily[day]["cost"]
        cumulative_cost.append(round(running_cost, 6))
    simulated_count = sum(
        1 for log in logs if log.is_simulated
    )
    dashboard_data = {
        "scatter": scatter_points,
        "dates": day_labels,
        "latency_over_time": daily_average_latency,
        "usage_over_time": daily_counts,
        "input_labels": list(INPUT_LABELS.values()),
        "input_counts": [
            method_counts[key] for key in INPUT_LABELS
        ],
        "token_by_input": [
            round(average_tokens_by_method[key], 1)
            for key in INPUT_LABELS
        ],
        "save_counts": [
            total_saved,
            max(total_extracted - total_saved, 0),
        ],
        "cost_over_time": cumulative_cost,
    }
    context = {
        "data": dashboard_data,
        "total_requests": total_requests,
        "average_latency": round(average_latency, 2),
        "average_tokens": round(average_tokens, 1),
        "average_cost": f"{average_cost:.6f}",
        "total_cost": f"{total_cost:.6f}",
        "save_rate": round(save_rate, 1),
        "simulated_count": simulated_count,
        "compute_rate": COMPUTE_RATE_PER_HOUR,
    }
    return render(
        request,
        "courses/analytics_dashboard.html",
        context,
    )
