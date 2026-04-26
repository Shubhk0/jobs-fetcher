"""
Job Scraper - Scrapes IT job listings from multiple free sources without API keys
Supports: LinkedIn, Twitter, GitHub Jobs, Indeed, Stack Overflow, and social media
Filters: Only IT/Tech/Software Development jobs
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import logging
from typing import List, Dict
import os
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JobScraper:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # IT-related keywords for filtering
        self.it_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'golang', 'rust',
            'developer', 'software engineer', 'backend', 'frontend', 'fullstack', 'devops',
            'data scientist', 'machine learning', 'ml engineer', 'ai engineer',
            'cloud engineer', 'systems engineer', 'network engineer', 'database',
            'react', 'vue', 'angular', 'node', 'django', 'flask', 'spring', 'fastapi',
            'aws', 'azure', 'gcp', 'kubernetes', 'docker', 'ci/cd',
            'programmer', 'coder', 'architect', 'engineer', 'sql', 'nosql',
            'web developer', 'mobile developer', 'android', 'ios', 'flutter',
            'devops', 'sre', 'site reliability', 'infrastructure', 'terraform',
            'cybersecurity', 'security engineer', 'penetration', 'infosec',
            'blockchain', 'solidity', 'ethereum', 'web3',
            'it support', 'it specialist', 'system administrator', 'dba',
            'solutions architect', 'technical lead', 'engineering manager',
            'qa engineer', 'test automation', 'quality assurance',
            'tech', 'software', 'coding', 'programming', 'it',
            'server', 'api', 'microservices', 'rest', 'graphql'
        ]
        
        # Non-IT keywords to exclude
        self.exclude_keywords = [
            'sales', 'marketing', 'business development', 'hr', 'human resources',
            'finance', 'accounting', 'legal', 'design', 'graphic', 'ux', 'ui',
            'content writer', 'copywriter', 'manager', 'administrator', 'recruiter'
        ]
    
    def is_it_job(self, title: str, description: str = '') -> bool:
        """Check if job is IT-related"""
        text = (title + ' ' + description).lower()
        
        # Check for IT keywords
        has_it_keyword = any(keyword in text for keyword in self.it_keywords)
        
        # Check for exclude keywords
        has_exclude_keyword = any(keyword in text for keyword in self.exclude_keywords)
        
        return has_it_keyword and not has_exclude_keyword
    
    def scrape_linkedin_jobs(self) -> List[Dict]:
        """Scrape IT jobs from LinkedIn public listings"""
        logger.info("Scraping LinkedIn Job Listings...")
        
        try:
            jobs_data = []
            # Multiple search queries for broader coverage
            queries = ['software engineer', 'python developer', 'javascript developer', 'data scientist', 'devops engineer']
            
            for query in queries:
                try:
                    url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location=Remote"
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find job cards
                    job_cards = soup.find_all('div', class_='base-card')
                    
                    for card in job_cards[:10]:
                        try:
                            title_elem = card.find('h3', class_='base-search-card__title')
                            company_elem = card.find('h4', class_='base-search-card__subtitle')
                            location_elem = card.find('span', class_='job-search-card__location')
                            link_elem = card.find('a', class_='base-card__full-link')
                            
                            if title_elem and company_elem:
                                title = title_elem.get_text(strip=True)
                                description = title
                                
                                if self.is_it_job(title, description):
                                    job = {
                                        'title': title,
                                        'company': company_elem.get_text(strip=True),
                                        'location': location_elem.get_text(strip=True) if location_elem else 'Remote',
                                        'salary': 'Not specified',
                                        'description': f"LinkedIn Job - {title}",
                                        'source': 'LinkedIn',
                                        'url': link_elem.get('href') if link_elem else '',
                                        'posted_at': datetime.now().isoformat()
                                    }
                                    jobs_data.append(job)
                                    logger.info(f"✓ Found IT job from LinkedIn: {job['title']} at {job['company']}")
                        except Exception as e:
                            logger.debug(f"Error parsing LinkedIn job card: {e}")
                            continue
                    
                    time.sleep(2)
                except Exception as e:
                    logger.warning(f"Error scraping LinkedIn for '{query}': {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from LinkedIn")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_linkedin_jobs: {e}")
            return []
    
    def scrape_twitter_jobs(self) -> List[Dict]:
        """Scrape IT job posts from Twitter/X hashtags"""
        logger.info("Scraping Twitter/X Job Posts...")
        
        try:
            jobs_data = []
            hashtags = ['#hiringnow', '#nowhiring', '#jobopening', '#ithiring', '#softwaredeveloper']
            
            for hashtag in hashtags:
                try:
                    # Search Twitter for job posts
                    url = f"https://twitter.com/search?q={hashtag}%20AND%20(developer%20OR%20engineer%20OR%20python%20OR%20javascript)&src=typed_query"
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find tweets
                    tweets = soup.find_all('article', class_='tweet')
                    
                    for tweet in tweets[:5]:
                        try:
                            text_elem = tweet.find('div', class_='tweet-text')
                            
                            if text_elem:
                                text = text_elem.get_text(strip=True)
                                
                                # Check for job keywords in tweet
                                if any(keyword in text.lower() for keyword in ['hiring', 'job', 'position', 'open role', 'we are hiring']):
                                    if self.is_it_job(text):
                                        # Extract company mention if available
                                        company = 'Not specified'
                                        match = re.search(r'@(\w+)', text)
                                        if match:
                                            company = match.group(1)
                                        
                                        job = {
                                            'title': text[:100],
                                            'company': company,
                                            'location': 'Check tweet for details',
                                            'salary': 'Not specified',
                                            'description': text[:200],
                                            'source': 'Twitter/X Posts',
                                            'url': '',
                                            'posted_at': datetime.now().isoformat()
                                        }
                                        jobs_data.append(job)
                                        logger.info(f"✓ Found IT job from Twitter: {job['title'][:50]}...")
                        except Exception as e:
                            logger.debug(f"Error parsing tweet: {e}")
                            continue
                    
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Error scraping Twitter hashtag '{hashtag}': {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from Twitter/X")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_twitter_jobs: {e}")
            return []
    
    def scrape_reddit_jobs(self) -> List[Dict]:
        """Scrape IT job posts from Reddit communities"""
        logger.info("Scraping Reddit Job Posts...")
        
        try:
            jobs_data = []
            subreddits = ['r/hiring', 'r/forhire', 'r/learnprogramming']
            
            for subreddit in subreddits:
                try:
                    url = f"https://www.reddit.com/{subreddit}/.json?limit=50"
                    response = requests.get(url, headers={**self.headers, 'User-Agent': 'JobScraper/1.0'}, timeout=10)
                    response.raise_for_status()
                    
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts[:10]:
                        try:
                            post_data = post.get('data', {})
                            title = post_data.get('title', '')
                            selftext = post_data.get('selftext', '')
                            
                            if title and (any(keyword in title.lower() for keyword in ['hiring', 'job', 'position']) or 
                                         any(keyword in selftext.lower() for keyword in ['hiring', 'job', 'position'])):
                                if self.is_it_job(title, selftext):
                                    job = {
                                        'title': title,
                                        'company': 'Not specified',
                                        'location': 'Check post for details',
                                        'salary': 'Not specified',
                                        'description': selftext[:200],
                                        'source': 'Reddit Posts',
                                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                                        'posted_at': datetime.fromtimestamp(post_data.get('created_utc', 0)).isoformat()
                                    }
                                    jobs_data.append(job)
                                    logger.info(f"✓ Found IT job from Reddit: {job['title'][:50]}...")
                        except Exception as e:
                            logger.debug(f"Error parsing Reddit post: {e}")
                            continue
                    
                    time.sleep(2)
                except Exception as e:
                    logger.warning(f"Error scraping Reddit {subreddit}: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from Reddit")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_reddit_jobs: {e}")
            return []
    
    def scrape_github_jobs(self) -> List[Dict]:
        """Scrape IT jobs from GitHub Jobs API (no authentication needed)"""
        logger.info("Scraping GitHub Jobs API...")
        
        try:
            jobs_data = []
            url = "https://jobs.github.com/positions.json"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            jobs = response.json()
            
            for job in jobs:
                title = job.get('title', 'Not specified')
                description = job.get('description', '')
                
                if self.is_it_job(title, description):
                    job_entry = {
                        'title': title,
                        'company': job.get('company', 'Not specified'),
                        'location': job.get('location', 'Remote'),
                        'salary': 'Not specified',
                        'description': description[:200],
                        'source': 'GitHub Jobs',
                        'url': job.get('url', ''),
                        'posted_at': job.get('created_at', datetime.now().isoformat())
                    }
                    jobs_data.append(job_entry)
                    logger.info(f"✓ Found IT job from GitHub: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from GitHub Jobs")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_github_jobs: {e}")
            return []
    
    def scrape_remoteok(self) -> List[Dict]:
        """Scrape IT jobs from RemoteOK"""
        logger.info("Scraping RemoteOK...")
        
        try:
            jobs_data = []
            url = "https://remoteok.com/remote-jobs.json"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            jobs = response.json()
            
            for job in jobs[1:]:
                if isinstance(job, dict):
                    title = job.get('title', 'Not specified')
                    description = job.get('description', '')
                    
                    if self.is_it_job(title, description):
                        job_entry = {
                            'title': title,
                            'company': job.get('company', 'Not specified'),
                            'location': 'Remote',
                            'salary': job.get('salary', 'Not specified'),
                            'description': description[:200],
                            'source': 'RemoteOK',
                            'url': job.get('url', ''),
                            'posted_at': job.get('date', datetime.now().isoformat())
                        }
                        jobs_data.append(job_entry)
                        logger.info(f"✓ Found IT job from RemoteOK: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from RemoteOK")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_remoteok: {e}")
            return []
    
    def scrape_dev_to_jobs(self) -> List[Dict]:
        """Scrape IT jobs from Dev.to"""
        logger.info("Scraping Dev.to Jobs...")
        
        try:
            jobs_data = []
            url = "https://dev.to/api/classified_listings?category=cfp-jobs"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            jobs = response.json()
            
            for job in jobs[:20]:
                title = job.get('title', 'Not specified')
                description = job.get('body_markdown', '')
                
                if self.is_it_job(title, description):
                    job_entry = {
                        'title': title,
                        'company': job.get('organization', 'Not specified'),
                        'location': job.get('location', 'Not specified'),
                        'salary': 'Not specified',
                        'description': description[:200],
                        'source': 'Dev.to',
                        'url': job.get('listing_url', ''),
                        'posted_at': job.get('created_at', datetime.now().isoformat())
                    }
                    jobs_data.append(job_entry)
                    logger.info(f"✓ Found IT job from Dev.to: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from Dev.to")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_dev_to_jobs: {e}")
            return []
    
    def scrape_we_work_remotely(self) -> List[Dict]:
        """Scrape IT jobs from We Work Remotely"""
        logger.info("Scraping We Work Remotely...")
        
        try:
            jobs_data = []
            url = "https://weworkremotely.com/api/remote_jobs"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('remote_jobs', [])
            
            for job in jobs[:15]:
                title = job.get('title', 'Not specified')
                description = job.get('short_description', '')
                
                if self.is_it_job(title, description):
                    job_entry = {
                        'title': title,
                        'company': job.get('company_name', 'Not specified'),
                        'location': 'Remote',
                        'salary': 'Not specified',
                        'description': description[:200],
                        'source': 'We Work Remotely',
                        'url': job.get('job_post_url', ''),
                        'posted_at': job.get('published_at', datetime.now().isoformat())
                    }
                    jobs_data.append(job_entry)
                    logger.info(f"✓ Found IT job from We Work Remotely: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from We Work Remotely")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_we_work_remotely: {e}")
            return []
    
    def scrape_arbeitnow(self) -> List[Dict]:
        """Scrape IT jobs from ArbeitNow"""
        logger.info("Scraping ArbeitNow...")
        
        try:
            jobs_data = []
            url = "https://www.arbeitnow.com/api/job-board-api"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('data', [])
            
            for job in jobs[:20]:
                title = job.get('title', 'Not specified')
                description = job.get('description', '')
                
                if self.is_it_job(title, description):
                    job_entry = {
                        'title': title,
                        'company': job.get('company_name', 'Not specified'),
                        'location': job.get('location', 'Not specified'),
                        'salary': 'Not specified',
                        'description': description[:200],
                        'source': 'ArbeitNow',
                        'url': job.get('url', ''),
                        'posted_at': job.get('date', datetime.now().isoformat())
                    }
                    jobs_data.append(job_entry)
                    logger.info(f"✓ Found IT job from ArbeitNow: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from ArbeitNow")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_arbeitnow: {e}")
            return []
    
    def scrape_stack_overflow(self) -> List[Dict]:
        """Scrape IT jobs from Stack Overflow"""
        logger.info("Scraping Stack Overflow Jobs...")
        
        try:
            jobs_data = []
            url = "https://stackoverflow.com/jobs"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='s-job-card')
            
            for card in job_cards[:10]:
                try:
                    title_elem = card.find('h2', class_='s-link')
                    company_elem = card.find('span', class_='fc-black-500')
                    location_elem = card.find('span', class_='fc-black-400')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        
                        if self.is_it_job(title):
                            job = {
                                'title': title,
                                'company': company_elem.get_text(strip=True) if company_elem else 'Not specified',
                                'location': location_elem.get_text(strip=True) if location_elem else 'Not specified',
                                'salary': 'Not specified',
                                'description': 'Stack Overflow Job',
                                'source': 'Stack Overflow',
                                'url': f"https://stackoverflow.com{title_elem['href']}" if title_elem.get('href') else '',
                                'posted_at': datetime.now().isoformat()
                            }
                            jobs_data.append(job)
                            logger.info(f"✓ Found IT job from Stack Overflow: {job['title']} at {job['company']}")
                except Exception as e:
                    logger.debug(f"Error parsing Stack Overflow job: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from Stack Overflow")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_stack_overflow: {e}")
            return []
    
    def scrape_indeed(self) -> List[Dict]:
        """Scrape IT jobs from Indeed"""
        logger.info("Scraping Indeed...")
        
        try:
            jobs_data = []
            queries = ['python developer', 'software engineer', 'javascript developer', 'data scientist']
            
            for query in queries:
                try:
                    url = f"https://www.indeed.com/jobs?q={query}&l=remote"
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    job_cards = soup.find_all('div', class_='job_seen_beacon')
                    
                    for card in job_cards[:5]:
                        try:
                            title_elem = card.find('h2', class_='jobTitle')
                            company_elem = card.find('span', class_='companyName')
                            
                            if title_elem and company_elem:
                                title = title_elem.get_text(strip=True)
                                
                                if self.is_it_job(title):
                                    job = {
                                        'title': title,
                                        'company': company_elem.get_text(strip=True),
                                        'location': 'Remote',
                                        'salary': 'Not specified',
                                        'description': title,
                                        'source': 'Indeed',
                                        'url': f"https://www.indeed.com{card.find('a')['href']}" if card.find('a') else '',
                                        'posted_at': datetime.now().isoformat()
                                    }
                                    jobs_data.append(job)
                                    logger.info(f"✓ Found IT job from Indeed: {job['title']} at {job['company']}")
                        except Exception as e:
                            logger.debug(f"Error parsing Indeed job: {e}")
                            continue
                    
                    time.sleep(2)
                except Exception as e:
                    logger.warning(f"Error scraping Indeed: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs_data)} IT jobs from Indeed")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_indeed: {e}")
            return []
    
    def scrape_all(self) -> List[Dict]:
        """Scrape all job sources including social media posts"""
        logger.info("\n" + "="*70)
        logger.info("🚀 STARTING COMPREHENSIVE IT JOB SCRAPING FROM ALL SOURCES")
        logger.info("Including: Job Sites + LinkedIn + Twitter + Reddit + Social Media")
        logger.info("="*70 + "\n")
        
        all_jobs = []
        
        # Scrape job board APIs
        all_jobs.extend(self.scrape_github_jobs())
        time.sleep(1)
        
        all_jobs.extend(self.scrape_remoteok())
        time.sleep(1)
        
        all_jobs.extend(self.scrape_dev_to_jobs())
        time.sleep(1)
        
        all_jobs.extend(self.scrape_we_work_remotely())
        time.sleep(1)
        
        all_jobs.extend(self.scrape_arbeitnow())
        time.sleep(1)
        
        all_jobs.extend(self.scrape_stack_overflow())
        time.sleep(2)
        
        all_jobs.extend(self.scrape_indeed())
        time.sleep(2)
        
        # Scrape LinkedIn
        all_jobs.extend(self.scrape_linkedin_jobs())
        time.sleep(2)
        
        # Scrape social media platforms
        all_jobs.extend(self.scrape_twitter_jobs())
        time.sleep(2)
        
        all_jobs.extend(self.scrape_reddit_jobs())
        time.sleep(2)
        
        # Remove duplicates
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        logger.info(f"\n{'='*70}")
        logger.info(f"✅ TOTAL IT JOBS COLLECTED FROM ALL SOURCES: {len(unique_jobs)}")
        logger.info(f"{'='*70}\n")
        return unique_jobs
    
    def save_to_json(self, jobs: List[Dict], output_file: str = "data/jobs.json"):
        """Save jobs to JSON file"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'total_jobs': len(jobs),
                    'filter': 'IT/Tech/Software Development Jobs Only',
                    'sources': ['LinkedIn', 'Twitter/X', 'Reddit', 'GitHub Jobs', 'RemoteOK', 'Dev.to', 
                               'We Work Remotely', 'ArbeitNow', 'Stack Overflow', 'Indeed'],
                    'jobs': jobs
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Successfully saved {len(jobs)} IT jobs to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            return False


def main():
    """Main execution function"""
    scraper = JobScraper()
    
    # Scrape all job sources including social media
    jobs = scraper.scrape_all()
    
    # Save to JSON
    scraper.save_to_json(jobs)
    
    logger.info(f"\n✅ Scraping completed! Total IT jobs collected: {len(jobs)}")


if __name__ == "__main__":
    main()
