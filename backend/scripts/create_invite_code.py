"""CLI to mint an invite code for invite-gated signup.

Usage: PYTHONPATH=backend:. python backend/scripts/create_invite_code.py [--max-uses N] [--note TEXT]
"""

from __future__ import annotations

import argparse
import asyncio
import secrets

from app.core.database import async_session_factory
from app.models import InviteCode


async def main(max_uses: int, note: str | None) -> None:
    code = secrets.token_urlsafe(8)
    async with async_session_factory() as db:
        db.add(InviteCode(code=code, max_uses=max_uses, note=note))
        await db.commit()
    print(f"Invite code created: {code} (max_uses={max_uses})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-uses", type=int, default=1)
    parser.add_argument("--note", type=str, default=None)
    args = parser.parse_args()
    asyncio.run(main(args.max_uses, args.note))
