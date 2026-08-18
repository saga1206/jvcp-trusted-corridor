from core.models import AuditEvent

def record(event_type, actor, entity_type, entity_id, **metadata):
    """Append-only, hash-chained audit trail. Tamper-evident prototype —
    NOT a blockchain, no distributed consensus, single database of record."""
    return AuditEvent.objects.create(
        actor=actor if (actor and actor.is_authenticated) else None,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=str(entity_id),
        metadata=metadata,
    )

def verify_chain():
    """Recomputes each event's hash from the stored data and confirms it still
    chains correctly — the actual tamper-detection check."""
    import hashlib, json
    events = AuditEvent.objects.order_by('id')
    prev_hash = '0' * 64
    for e in events:
        payload = json.dumps({
            "actor": e.actor_id,
            "event_type": e.event_type,
            "entity_type": e.entity_type,
            "entity_id": e.entity_id,
            "metadata": e.metadata,
            "previous_hash": e.previous_hash,
        }, sort_keys=True, default=str)
        recomputed = hashlib.sha256(payload.encode()).hexdigest()
        if e.previous_hash != prev_hash or recomputed != e.event_hash:
            return {"valid": False, "broken_at_event_id": e.id}
        prev_hash = e.event_hash
    return {"valid": True, "events_checked": events.count()}