"""
Job Scraper - Scrapes job listings from multiple free sources without API keys
Supports: Indeed, LinkedIn, GitHub Jobs, Stack Overflow, and more
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import logging
from typing import List, Dict
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JobScraper:
    def __init__(self):
        self.jobs = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_indeed(self, query: str = "software engineer", location: str = "remote", pages: int = 3) -> List[Dict]:
        """Scrape jobs from Indeed without API key"""
        logger.info(f"Scraping Indeed for '{query}' in {location}...")
        
        try:
            jobs_data = []
            for page in range(pages):
                url = f"https://www.indeed.com/jobs?q={query}&l={location}&start={page * 10}"
                
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find all job cards
                    job_cards = soup.find_all('div', class_='job_seen_beacon')
                    
                    for card in job_cards:
                        try:
                            title_elem = card.find('h2', class_='jobTitle')
                            company_elem = card.find('span', class_='companyName')
                            location_elem = card.find('div', class_='companyLocation')
                            salary_elem = card.find('div', class_='salary-snippet')
                            summary_elem = card.find('div', class_='job-snippet')
                            
                            if title_elem and company_elem:
                                job = {
                                    'title': title_elem.get_text(strip=True),
                                    'company': company_elem.get_text(strip=True),
                                    'location': location_elem.get_text(strip=True) if location_elem else 'Not specified',
                                    'salary': salary_elem.get_text(strip=True) if salary_elem else 'Not specified',
                                    'description': summary_elem.get_text(strip=True) if summary_elem else 'No description',
                                    'source': 'Indeed',
                                    'url': f"https://www.indeed.com{card.find('a')['href']}" if card.find('a') else '',
                                    'posted_at': datetime.now().isoformat()
                                }
                                jobs_data.append(job)
                                logger.info(f"Found: {job['title']} at {job['company']}")
                        except Exception as e:
                            logger.debug(f"Error parsing job card: {e}")
                            continue
                    
                    time.sleep(2)  # Be respectful to the server
                    
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Error scraping Indeed page {page}: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs_data)} jobs from Indeed")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_indeed: {e}")
            return []
    
    def scrape_github_jobs(self) -> List[Dict]:
        """Scrape jobs from GitHub Jobs API (no authentication needed)"""
        logger.info("Scraping GitHub Jobs API...")
        
        try:
            jobs_data = []
            url = "https://jobs.github.com/positions.json"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            jobs = response.json()
            
            for job in jobs:
                job_entry = {
                    'title': job.get('title', 'Not specified'),
                    'company': job.get('company', 'Not specified'),
                    'location': job.get('location', 'Remote'),
                    'salary': 'Not specified',
                    'description': job.get('description', '')[:200],
                    'source': 'GitHub Jobs',
                    'url': job.get('url', ''),
                    'posted_at': job.get('created_at', datetime.now().isoformat())
                }
                jobs_data.append(job_entry)
                logger.info(f"Found: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} jobs from GitHub Jobs")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_github_jobs: {e}")
            return []
    
    def scrape_stack_overflow(self) -> List[Dict]:
        """Scrape jobs from Stack Overflow"""
        logger.info("Scraping Stack Overflow Jobs...")
        
        try:
            jobs_data = []
            url = "https://stackoverflow.com/jobs"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings
            job_cards = soup.find_all('div', class_='s-job-card')
            
            for card in job_cards[:10]:  # Limit to 10 jobs
                try:
                    title_elem = card.find('h2', class_='s-link')
                    company_elem = card.find('span', class_='fc-black-500')
                    location_elem = card.find('span', class_='fc-black-400')
                    
                    if title_elem:
                        job = {
                            'title': title_elem.get_text(strip=True),
                            'company': company_elem.get_text(strip=True) if company_elem else 'Not specified',
                            'location': location_elem.get_text(strip=True) if location_elem else 'Not specified',
                            'salary': 'Not specified',
                            'description': 'Stack Overflow Job',
                            'source': 'Stack Overflow',
                            'url': f"https://stackoverflow.com{title_elem['href']}" if title_elem.get('href') else '',
                            'posted_at': datetime.now().isoformat()
                        }
                        jobs_data.append(job)
                        logger.info(f"Found: {job['title']} at {job['company']}")
                except Exception as e:
                    logger.debug(f"Error parsing Stack Overflow job: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs_data)} jobs from Stack Overflow")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_stack_overflow: {e}")
            return []
    
    def scrape_remoteok(self) -> List[Dict]:
        """Scrape jobs from RemoteOK (no API key needed for basic scraping)"""
        logger.info("Scraping RemoteOK...")
        
        try:
            jobs_data = []
            url = "https://remoteok.com/remote-jobs.json"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            jobs = response.json()
            
            for job in jobs[1:]:  # Skip first item (header)
                if isinstance(job, dict):
                    job_entry = {
                        'title': job.get('title', 'Not specified'),
                        'company': job.get('company', 'Not specified'),
                        'location': 'Remote',
                        'salary': job.get('salary', 'Not specified'),
                        'description': job.get('description', '')[:200],
                        'source': 'RemoteOK',
                        'url': job.get('url', ''),
                        'posted_at': job.get('date', datetime.now().isoformat())
                    }
                    jobs_data.append(job_entry)
                    logger.info(f"Found: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} jobs from RemoteOK")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_remoteok: {e}")
            return []
    
    def scrape_dev_to_jobs(self) -> List[Dict]:
        """Scrape jobs from Dev.to API (free, no key required)"""
        logger.info("Scraping Dev.to Jobs...")
        
        try:
            jobs_data = []
            url = "https://dev.to/api/classified_listings?category=cfp-jobs"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            jobs = response.json()
            
            for job in jobs[:20]:  # Limit to 20 jobs
                job_entry = {
                    'title': job.get('title', 'Not specified'),
                    'company': job.get('organization', 'Not specified'),
                    'location': job.get('location', 'Not specified'),
                    'salary': 'Not specified',
                    'description': job.get('body_markdown', '')[:200],
                    'source': 'Dev.to',
                    'url': job.get('listing_url', ''),
                    'posted_at': job.get('created_at', datetime.now().isoformat())
                }
                jobs_data.append(job_entry)
                logger.info(f"Found: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} jobs from Dev.to")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_dev_to_jobs: {e}")
            return []
    
    def scrape_we_work_remotely(self) -> List[Dict]:
        """Scrape jobs from We Work Remotely API"""
        logger.info("Scraping We Work Remotely...")
        
        try:
            jobs_data = []
            url = "https://weworkremotely.com/api/remote_jobs"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('remote_jobs', [])
            
            for job in jobs[:15]:  # Limit to 15 jobs
                job_entry = {
                    'title': job.get('title', 'Not specified'),
                    'company': job.get('company_name', 'Not specified'),
                    'location': 'Remote',
                    'salary': 'Not specified',
                    'description': job.get('short_description', '')[:200],
                    'source': 'We Work Remotely',
                    'url': job.get('job_post_url', ''),
                    'posted_at': job.get('published_at', datetime.now().isoformat())
                }
                jobs_data.append(job_entry)
                logger.info(f"Found: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} jobs from We Work Remotely")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_we_work_remotely: {e}")
            return []
    
    def scrape_arbeitnow(self) -> List[Dict]:
        """Scrape jobs from ArbeitNow (free API)"""
        logger.info("Scraping ArbeitNow...")
        
        try:
            jobs_data = []
            url = "https://www.arbeitnow.com/api/job-board-api"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('data', [])
            
            for job in jobs[:20]:  # Limit to 20 jobs
                job_entry = {
                    'title': job.get('title', 'Not specified'),
                    'company': job.get('company_name', 'Not specified'),
                    'location': job.get('location', 'Not specified'),
                    'salary': 'Not specified',
                    'description': job.get('description', '')[:200],
                    'source': 'ArbeitNow',
                    'url': job.get('url', ''),
                    'posted_at': job.get('date', datetime.now().isoformat())
                }
                jobs_data.append(job_entry)
                logger.info(f"Found: {job_entry['title']} at {job_entry['company']}")
            
            logger.info(f"Successfully scraped {len(jobs_data)} jobs from ArbeitNow")
            return jobs_data
            
        except Exception as e:
            logger.error(f"Error in scrape_arbeitnow: {e}")
            return []
    
    def scrape_all(self) -> List[Dict]:
        """Scrape all job sources"""
        logger.info("Starting comprehensive job scraping from all sources...")
        
        all_jobs = []
        
        # Scrape from free APIs (no key required)
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
        
        # Scrape HTML-based sources
        all_jobs.extend(self.scrape_stack_overflow())
        time.sleep(2)
        
        all_jobs.extend(self.scrape_indeed(query="software engineer", location="remote", pages=2))
        time.sleep(2)
        
        # Remove duplicates
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = (job['title'], job['company'])
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        logger.info(f"Total jobs scraped from all sources: {len(unique_jobs)}")
        return unique_jobs
    
    def save_to_json(self, jobs: List[Dict], output_file: str = "data/jobs.json"):
        """Save jobs to JSON file"""
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'total_jobs': len(jobs),
                    'jobs': jobs
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully saved {len(jobs)} jobs to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            return False


def main():
    """Main execution function"""
    scraper = JobScraper()
    
    # Scrape all job sources
    jobs = scraper.scrape_all()
    
    # Save to JSON
    scraper.save_to_json(jobs)
    
    logger.info(f"\n✅ Scraping completed! Total jobs collected: {len(jobs)}")


if __name__ == "__main__":
    main()
