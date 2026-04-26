import json
import os
from collections import Counter

def generate_stats():
    os.makedirs('docs', exist_ok=True)

    try:
        with open('data/jobs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("data/jobs.json not found.")
        return

    jobs = data.get('jobs', [])

    sources = Counter(job.get('source') for job in jobs)

    with open('docs/STATS.md', 'w', encoding='utf-8') as f:
        f.write("# Job Statistics\n\n")
        f.write(f"**Total Jobs:** {data.get('total_jobs', 0)}\n\n")
        f.write(f"**Last Updated:** {data.get('timestamp', 'N/A')}\n\n")

        f.write("## Jobs by Source\n\n")
        for source, count in sources.most_common():
            f.write(f"- **{source}:** {count}\n")

    print("Stats generated at docs/STATS.md")

if __name__ == "__main__":
    generate_stats()
