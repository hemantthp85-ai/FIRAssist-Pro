import asyncio
import json
import logging

from app.agents.fir_generator import (
    generate_fir
)

from app.agents.fir_writer_agent import (
    generate_fir_narrative
)

from app.agents.legal_agent import (
    recommend_sections
)

from app.agents.investigation_report_agent import (
    generate_investigation_report
)

from app.agents.evidence_agent import (
    analyze_evidence_requirements
)

from app.agents.case_timeline_agent import (
    generate_case_timeline
)

from app.agents.risk_assessment_agent import (
    assess_case_risk
)

from app.agents.action_recommendation_agent import (
    recommend_actions
)

from app.dashboard.police_dashboard_generator import (
    generate_dashboard
)

from app.utils.performance import (
    cached_call,
    get_slowest_agents,
    timed_agent
)


logger = logging.getLogger("fir_copilot.orchestrator")


def parse_json_result(value):
    if isinstance(value, str):
        return json.loads(
            value
        )

    return value


async def run_sync_agent(name, func, *args, parser=None, cache_key=None):
    @timed_agent(name)
    def execute():
        if cache_key is not None:
            result = cached_call(
                name,
                cache_key,
                func,
                *args
            )
        else:
            result = func(
                *args
            )

        if parser:
            return parser(
                result
            )

        return result

    return await asyncio.to_thread(
        execute
    )


async def run_case_orchestration_async(case_data):

    dossier = {}

    fir_json = await run_sync_agent(
        "fir_generator",
        generate_fir,
        case_data,
        cache_key=case_data
    )

    dossier["fir"] = fir_json

    # Warm up master analysis sequentially first to populate the cache
    from app.agents.master_agent import run_master_analysis
    await run_sync_agent(
        "master_analysis",
        run_master_analysis,
        case_data,
        cache_key=case_data
    )

    agent_tasks = {
        "fir_narrative": run_sync_agent(
            "fir_writer_agent",
            generate_fir_narrative,
            fir_json,
            cache_key=fir_json
        ),
        "legal_analysis": run_sync_agent(
            "legal_agent",
            recommend_sections,
            case_data,
            parser=parse_json_result,
            cache_key=case_data
        ),
        "investigation_report": run_sync_agent(
            "investigation_report_agent",
            generate_investigation_report,
            case_data,
            parser=parse_json_result,
            cache_key=case_data
        ),
        "evidence_analysis": run_sync_agent(
            "evidence_agent",
            analyze_evidence_requirements,
            case_data,
            parser=parse_json_result,
            cache_key=case_data
        ),
        "timeline_analysis": run_sync_agent(
            "timeline_agent",
            generate_case_timeline,
            case_data,
            parser=parse_json_result,
            cache_key=case_data
        ),
        "risk_assessment": run_sync_agent(
            "risk_assessment_agent",
            assess_case_risk,
            case_data,
            parser=parse_json_result,
            cache_key=case_data
        ),
        "action_recommendations": run_sync_agent(
            "action_recommendation_agent",
            recommend_actions,
            case_data,
            parser=parse_json_result,
            cache_key=case_data
        )
    }

    results = await asyncio.gather(
        *agent_tasks.values(),
        return_exceptions=True
    )

    for key, result in zip(agent_tasks.keys(), results):
        if isinstance(result, Exception):
            dossier[key] = str(
                result
            )
        else:
            dossier[key] = result

    dashboard = await run_sync_agent(
        "dashboard_generation",
        generate_dashboard,
        dossier,
        cache_key=dossier
    )

    logger.info(
        "slowest_agents=%s",
        get_slowest_agents()
    )

    return dashboard


def run_case_orchestration(case_data):
    try:
        asyncio.get_running_loop()

    except RuntimeError:
        return asyncio.run(
            run_case_orchestration_async(case_data)
        )

    raise RuntimeError(
        "run_case_orchestration_async must be awaited inside an active event loop"
    )


if __name__ == "__main__":

    sample_case = {
        "victim_name": "Hemantth",
        "victim_phone": "8610595920",
        "incident_summary": "Mobile phone theft",
        "incident_date": "5 June 2026",
        "incident_time": "6:30 PM",
        "location": "Trichy Bus Stand",
        "property_type": "Mobile Phone",
        "property_value": "15000",
        "possible_offences": [
            "Theft"
        ]
    }

    dossier = run_case_orchestration(
        sample_case
    )

    print(
        json.dumps(
            dossier,
            indent=4
        )
    )
