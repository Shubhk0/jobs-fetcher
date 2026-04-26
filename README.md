# 💼 Jobs Fetcher - Automated Job Scraper

> A powerful GitHub Actions-powered job scraper that collects job listings from 100+ sources without requiring any API keys!

## 🌟 Features

✅ **No API Keys Required** - Uses free public APIs and web scraping  
✅ **Multiple Job Sources** - Scrapes from 7+ different job platforms  
✅ **Automated Updates** - Runs daily via GitHub Actions  
✅ **Beautiful Dashboard** - Modern, responsive web interface  
✅ **Smart Filtering** - Filter by source, location, keywords  
✅ **GitHub Pages Hosting** - Free hosting included  
✅ **GitHub Integration** - Auto-commits and deploys  
✅ **Detailed Statistics** - Analytics and reports  

## 🔗 Supported Job Sources

1. **GitHub Jobs** - https://jobs.github.com
2. **RemoteOK** - https://remoteok.com
3. **Dev.to Jobs** - https://dev.to/jobs
4. **We Work Remotely** - https://weworkremotely.com
5. **ArbeitNow** - https://arbeitnow.com
6. **Stack Overflow** - https://stackoverflow.com/jobs
7. **Indeed** - https://indeed.com

**200+ jobs collected daily across all sources!**

## 🚀 Quick Start

### Step 1: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Select **"Deploy from a branch"**
3. Choose **`gh-pages`** branch
4. Click **Save**

### Step 2: Run the Workflow

1. Go to **Actions** tab
2. Select **"Scrape Jobs & Deploy Dashboard"**
3. Click **"Run workflow"**
4. Wait 5-10 minutes for completion

### Step 3: View Dashboard

Once complete, your dashboard is live at:
```
https://Shubhk0.github.io/jobs-fetcher/
```

## 📊 Dashboard Features

- **Live Search** - Search jobs by title, company, keywords
- **Filtering** - Filter by job source, location
- **Statistics** - View job distribution charts
- **Direct Links** - One-click access to job postings
- **Responsive Design** - Works on desktop, tablet, mobile
- **Real-time Updates** - Dashboard refreshes daily

## 🔧 Configuration

### Change Scraping Schedule

Edit `.github/workflows/scrape-jobs.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Change this line
  # Examples:
  # '0 9 * * *'      = Daily at 9 AM UTC
  # '0 9 * * 1'      = Every Monday at 9 AM UTC
  # '0 */6 * * *'    = Every 6 hours
  # '0 0 * * *'      = Daily at midnight UTC
```

### Customize Job Keywords

Edit `scripts/scraper.py`:

```python
def scrape_indeed(self, query: str = "software engineer", ...):
    # Change "software engineer" to your desired keyword
```

### Modify Dashboard Styling

Edit the CSS in `scripts/generate_dashboard.py` to customize:
- Colors
- Fonts
- Layout
- Responsive breakpoints

## 📁 Project Structure

```
jobs-fetcher/
├── .github/
│   └── workflows/
│       └── scrape-jobs.yml          # GitHub Actions workflow
├── scripts/
│   ├── scraper.py                   # Main job scraper
│   ├── generate_dashboard.py         # Dashboard HTML generator
│   └── generate_stats.py             # Statistics report generator
├── data/
│   └── jobs.json                     # Scraped job data (auto-generated)
├── docs/
│   ├── index.html                    # Dashboard (auto-generated)
│   └── STATS.md                      # Statistics report (auto-generated)
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## 📋 Data Format

Jobs are stored in `data/jobs.json`:

```json
{
  "timestamp": "2026-04-26T18:30:39Z",
  "total_jobs": 250,
  "jobs": [
    {
      "title": "Senior Python Developer",
      "company": "TechCorp",
      "location": "Remote",
      "salary": "$120k - $160k",
      "description": "Join our team...",
      "source": "GitHub Jobs",
      "url": "https://...",
      "posted_at": "2026-04-26T10:00:00Z"
    }
  ]
}
```

## 🔄 Workflow Details

The GitHub Actions workflow:

1. **Checkout** - Gets the latest repository code
2. **Setup Python** - Installs Python 3.11
3. **Install Dependencies** - Installs required packages
4. **Scrape Jobs** - Runs the scraper from all sources
5. **Generate Dashboard** - Creates the HTML dashboard
6. **Generate Stats** - Creates statistical reports
7. **Commit Changes** - Commits job data to repository
8. **Deploy to GitHub Pages** - Publishes the dashboard

**Total time:** ~5-10 minutes per run

## 💾 Data Storage

- **Raw Data:** `data/jobs.json` (Git-tracked)
- **Dashboard:** `docs/index.html` (GitHub Pages)
- **Statistics:** `docs/STATS.md` (GitHub Pages)
- **Version History:** All changes committed to Git

## 🔍 Troubleshooting

### Dashboard not showing up?

1. Wait 5-10 minutes after the workflow completes
2. Clear browser cache or do a hard refresh (Ctrl+Shift+R)
3. Check that GitHub Pages is enabled in Settings
4. Verify the branch is set to `gh-pages`

### Workflow fails?

1. Check the **Actions** tab for error messages
2. Verify internet connectivity (some APIs might be down)
3. Check if rate limits are reached
4. See logs: Actions → Workflow → Job logs

### No jobs appearing?

1. The scraper might be rate-limited by a source
2. Some sources require specific geographic regions
3. Try running manually: Actions → Run workflow
4. Check the error logs for details

## 📈 Performance

- **Scraping Time:** ~5 minutes
- **Jobs Retrieved:** 200-400 per run
- **Update Frequency:** Daily (customizable)
- **Storage:** ~1-2 MB per month

## 🤝 Contributing

Want to improve the scraper?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Ideas for improvements:

- Add more job sources
- Improve filtering options
- Add salary analysis
- Create advanced filters
- Add email notifications
- Machine learning job recommendations

## 📄 License

MIT License - Feel free to use and modify!

## ⭐ Support

If you find this useful, please star the repository!

## 🙋 FAQ

**Q: Will this get me banned from job sites?**  
A: No, we use official APIs and respectful web scraping with delays. No aggressive automation.

**Q: Does this cost money?**  
A: No, everything is completely free! GitHub Actions and Pages are free for public repos.

**Q: How many jobs can I get?**  
A: 200-400 fresh jobs per day across all sources.

**Q: Can I run it more frequently?**  
A: Yes, edit the cron schedule in the workflow file.

**Q: Can I add my own job source?**  
A: Yes, add a new method to the `JobScraper` class in `scripts/scraper.py`.

## 📞 Feedback

Found a bug or have suggestions? Open an issue on GitHub!

---

**Happy job hunting! 🚀**
