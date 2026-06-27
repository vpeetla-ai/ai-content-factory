"""Redis key patterns per architecture Data & DB tab."""

PIPELINE_STATE = "pipeline:state:{run_id}"
RATELIMIT = "ratelimit:{user_id}:{minute}"
HITL_PENDING = "hitl:pending:{run_id}"
RESEARCH_CACHE = "cache:research:{topic_hash}"
PUBLISH_QUEUE = "queue:publish"
SESSION = "session:{session_id}"
