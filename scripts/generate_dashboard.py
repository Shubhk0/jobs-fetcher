import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

def generate_dashboard():
    # Ensure docs directory exists
    os.makedirs('docs', exist_ok=True)

    # Load job data
    try:
        with open('data/jobs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("data/jobs.json not found. Creating empty data.")
        data = {"jobs": [], "total_jobs": 0, "timestamp": ""}

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IT Jobs Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    </head>
    <body class="bg-gray-100 font-sans">
        <div class="container mx-auto p-4">
            <header class="bg-white shadow rounded p-6 mb-6">
                <h1 class="text-3xl font-bold text-gray-800">💼 IT Jobs Dashboard</h1>
                <p class="text-gray-600 mt-2">Total Jobs: {{ data.total_jobs }} | Last Updated: {{ data.timestamp }}</p>
            </header>

            <div class="flex flex-wrap gap-4 mb-6">
                <input type="text" id="searchInput" placeholder="Search jobs by title or company..." class="p-2 border rounded w-full md:w-1/2">
                <select id="sourceFilter" class="p-2 border rounded w-full md:w-1/4">
                    <option value="all">All Sources</option>
                    {% for source in sources %}
                        <option value="{{ source }}">{{ source }}</option>
                    {% endfor %}
                </select>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="jobContainer">
                {% for job in data.jobs %}
                <div class="bg-white rounded shadow p-6 job-card" data-title="{{ job.title | lower }}" data-company="{{ job.company | lower }}" data-source="{{ job.source }}">
                    <h2 class="text-xl font-semibold text-blue-600 mb-2">{{ job.title }}</h2>
                    <p class="text-gray-700 font-medium mb-1">{{ job.company }}</p>
                    <p class="text-sm text-gray-500 mb-1">📍 {{ job.location }}</p>
                    <p class="text-sm text-gray-500 mb-3">🏢 {{ job.source }}</p>
                    <div class="mt-4">
                        <a href="{{ job.url }}" target="_blank" class="inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">Apply Now</a>
                    </div>
                </div>
                {% endfor %}
            </div>

            <div id="noResults" class="hidden text-center text-gray-600 py-10">
                <p class="text-xl">No jobs found matching your criteria.</p>
            </div>
        </div>

        <script>
            const searchInput = document.getElementById('searchInput');
            const sourceFilter = document.getElementById('sourceFilter');
            const jobCards = document.querySelectorAll('.job-card');
            const noResults = document.getElementById('noResults');

            function filterJobs() {
                const searchTerm = searchInput.value.toLowerCase();
                const selectedSource = sourceFilter.value;
                let visibleCount = 0;

                jobCards.forEach(card => {
                    const title = card.getAttribute('data-title');
                    const company = card.getAttribute('data-company');
                    const source = card.getAttribute('data-source');

                    const matchesSearch = title.includes(searchTerm) || company.includes(searchTerm);
                    const matchesSource = selectedSource === 'all' || source === selectedSource;

                    if (matchesSearch && matchesSource) {
                        card.style.display = 'block';
                        visibleCount++;
                    } else {
                        card.style.display = 'none';
                    }
                });

                if (visibleCount === 0) {
                    noResults.classList.remove('hidden');
                } else {
                    noResults.classList.add('hidden');
                }
            }

            searchInput.addEventListener('input', filterJobs);
            sourceFilter.addEventListener('change', filterJobs);
        </script>
    </body>
    </html>
    """

    # Extract unique sources
    sources = list(set([job.get('source') for job in data.get('jobs', []) if job.get('source')]))
    sources.sort()

    from jinja2 import Template
    template = Template(html_template)
    html_content = template.render(data=data, sources=sources)

    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Dashboard generated at docs/index.html")

if __name__ == "__main__":
    generate_dashboard()
