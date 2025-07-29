complex_workflow_with_pos = {
    "workflow": {
        "tasks": [
            {
                "id": "task_ingest",
                "name": "Ingest Data",
                "size_box": [150, 60],
                "inputs": [],
                "outputs": ["raw_records"],
                "inputs_pos": [],
                "outputs_pos": [0.5],
            },
            {
                "id": "task_validate",
                "name": "Validate Schema",
                "size_box": [150, 80],
                "inputs": ["records_in"],
                "outputs": ["valid_records", "invalid_records"],
                "inputs_pos": [0.5],
                "outputs_pos": [0.2, 0.8],
            },
            {
                "id": "task_log_errors",
                "name": "Log Errors",
                "size_box": [150, 60],
                "inputs": ["failed_records"],
                "outputs": ["logged_errors"],
                "inputs_pos": [0.5],
                "outputs_pos": [0.5],
            },
            {
                "id": "task_reprocess",
                "name": "Reprocess Failed",
                "size_box": [150, 60],
                "inputs": ["errors_to_fix"],
                "outputs": ["fixed_records"],
                "inputs_pos": [0.5],
                "outputs_pos": [0.5],
            },
            {
                "id": "task_enrich",
                "name": "Enrich with API",
                "size_box": [150, 80],
                "inputs": ["validated_records"],
                "outputs": ["enriched_data", "api_latency"],
                "inputs_pos": [0.5],
                "outputs_pos": [0.2, 0.8],
            },
            {
                "id": "task_aggregate",
                "name": "Aggregate Results",
                "size_box": [150, 60],
                "inputs": ["final_data"],
                "outputs": ["report_data"],
                "inputs_pos": [0.5],
                "outputs_pos": [0.5],
            },
            {
                "id": "task_report",
                "name": "Generate Report",
                "size_box": [150, 60],
                "inputs": ["aggregated_data"],
                "outputs": [],
                "inputs_pos": [0.5],
                "outputs_pos": [],
            },
            {
                "id": "task_monitor",
                "name": "Monitor Latency",
                "size_box": [150, 60],
                "inputs": ["latency_data"],
                "outputs": [],
                "inputs_pos": [0.5],
                "outputs_pos": [],
            },
        ],
        "links": [
            # Main path
            {
                "source": {"task_id": "task_ingest", "output_name": "raw_records"},
                "target": {"task_id": "task_validate", "input_name": "records_in"},
            },
            {
                "source": {"task_id": "task_validate", "output_name": "valid_records"},
                "target": {"task_id": "task_enrich", "input_name": "validated_records"},
            },
            {
                "source": {"task_id": "task_enrich", "output_name": "enriched_data"},
                "target": {"task_id": "task_aggregate", "input_name": "final_data"},
            },
            {
                "source": {"task_id": "task_aggregate", "output_name": "report_data"},
                "target": {"task_id": "task_report", "input_name": "aggregated_data"},
            },
            # Monitoring branch
            {
                "source": {"task_id": "task_enrich", "output_name": "api_latency"},
                "target": {"task_id": "task_monitor", "input_name": "latency_data"},
            },
            # Cyclic error-handling loop
            {
                "source": {
                    "task_id": "task_validate",
                    "output_name": "invalid_records",
                },
                "target": {
                    "task_id": "task_log_errors",
                    "input_name": "failed_records",
                },
            },
            {
                "source": {
                    "task_id": "task_log_errors",
                    "output_name": "logged_errors",
                },
                "target": {"task_id": "task_reprocess", "input_name": "errors_to_fix"},
            },
            {
                "source": {"task_id": "task_reprocess", "output_name": "fixed_records"},
                "target": {"task_id": "task_validate", "input_name": "records_in"},
            },
        ],
    }
}
