#!/usr/bin/env python
"""
Generate synthetic historical ticket files for Task 16 RAG Arch.

Creates 200 plain-text .txt files in the data/historical_tickets folder.
Each file represents a support ticket with:
- Ticket ID
- Issue
- Conversation (multiple back-and-forth messages)
- Resolution
- Status

Some tickets are made long to test chunking.
"""

import os
import random
from pathlib import Path

# Folder where tickets will be written
TICKETS_DIR = Path(__file__).parent.parent / "data" / "historical_tickets"
TICKETS_DIR.mkdir(parents=True, exist_ok=True)

# Sample data for generating realistic-ish tickets
ISSUES = [
    "User cannot stay logged into application.",
    "Application crashes when opening a specific file.",
    "Print job fails with error code 0x80004005.",
    "Unable to send emails after password change.",
    "VPN connection drops intermittently.",
    "Software license validation fails after reboot.",
    "Database connection timeout during peak hours.",
    "Mobile app fails to sync with server.",
    "Error 404 when accessing internal portal.",
    "Unexpected shutdown during data export."
]

RESOLUTIONS = [
    "Updated session timeout configuration.",
    "Reinstalled the latest patch from vendor.",
    "Reset the print spooler service.",
    "Updated SMTP credentials in the email client.",
    "Reconfigured VPN client with new gateway settings.",
    "Renewed the license key and reactivated.",
    "Increased database connection pool size.",
    "Cleared app cache and forced a fresh sync.",
    "Corrected the URL rewrite rule in IIS.",
    "Applied Windows update and checked hardware."
]

STATUSES = ["Resolved", "Open", "In Progress", "Closed"]

def generate_ticket(ticket_num: int) -> str:
    ticket_id = f"INC{1000 + ticket_num:04d}"
    issue = random.choice(ISSUES)
    resolution = random.choice(RESOLUTIONS)
    status = random.choice(STATUSES)

    # Generate a conversation with a random number of segments (2 to 8)
    num_segments = random.randint(2, 8)
    conversation_lines = []
    for i in range(num_segments):
        speaker = "Customer" if i % 2 == 0 else "Agent"
        # Make some segments longer to simulate detailed exchanges
        if random.random() < 0.3:
            # Longer message
            msg = f"This is a detailed message from the {speaker.lower()} about the issue. " \
                  f"It includes multiple sentences and some technical details. " \
                  f"We need to consider various factors such as environment, configuration, and logs."
        else:
            # Shorter message
            msg = f"{speaker}: Brief update on the situation."
        conversation_lines.append(msg)

    conversation = "\n".join(conversation_lines)

    # Occasionally make a ticket very long by adding many segments or long messages
    if random.random() < 0.1:  # 10% chance of extra long ticket
        extra_segments = "\n".join([
            f"Agent: Additional troubleshooting steps performed.",
            f"Customer: Provided more logs and screenshots.",
            f"Agent: Analyzed the logs and found a root cause in the configuration.",
            f"Customer: Confirmed the issue occurs on multiple machines.",
            f"Agent: Developed a fix and tested in a staging environment.",
            f"Customer: Verified the fix resolves the problem.",
            f"Agent: Prepared rollout plan for production."
        ])
        conversation = conversation + "\n" + extra_segments

    ticket_content = f"""Ticket ID: {ticket_id}

Issue:
{issue}

Conversation:
{conversation}

Resolution:
{resolution}

Status:
{status}
"""
    return ticket_content

def main():
    print(f"Generating 200 ticket files in {TICKETS_DIR}...")
    for i in range(200):
        content = generate_ticket(i)
        file_path = TICKETS_DIR / f"INC{1000 + i:04d}.txt"
        file_path.write_text(content, encoding='utf-8')
        if (i + 1) % 50 == 0:
            print(f"  Generated {i + 1} files...")
    print("Done.")

if __name__ == "__main__":
    main()