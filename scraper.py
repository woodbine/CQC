# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
import csv
import re
import requests

def connect(url):
    
    report_soup = ''
    try:
        report_html = requests.get(url, timeout = 60)
        report_soup = BeautifulSoup(report_html.text, 'lxml')
    except:
        print url
        # connect(url)
    while not report_soup:
        report_soup = ''
        try:
            report_html = requests.get(url, timeout = 60)
            report_soup = BeautifulSoup(report_html.text, 'lxml')
            print report_soup.title
        except:
            pass  

    return report_soup

directoryUrl = "http://www.cqc.org.uk/content/how-get-and-re-use-cqc-information-and-data#directory"
# html = urllib2.urlopen(directoryUrl)
# soup = BeautifulSoup(html)
soup = connect(directoryUrl)

block = soup.find('div',{'id':'directory'})
csvA = block.find('a',href=True)
csvUrl = csvA['href']
print csvUrl
response = urllib2.urlopen(csvUrl)
csv_file = csv.reader(response)
p = 0
for row in csv_file:
    if 'http' not in row[12]:
        continue
    print p
    location_url = row[12].replace('https://admin.cqc.org.uk', 'http://www.cqc.org.uk')
    name = row[0]
    add1 = ' '.join(row[2].split(',')[:-1])
    add2 = row[2].split(',')[-1]
    add3 = row[10]
    add4 = row[11]
    postal_code = row[3]
    telephone = row[4]
    type_of_service = row[6]
    services = row[8]
    local_authority = row[11]
    cqc_id = row[14]
    # print name, cqc_id
    # report_html = urllib2.urlopen(location_url)
    # report_soup = BeautifulSoup(report_html)
    report_soup = connect(location_url)
    latest_report_url = location_url+'/reports'
    latest_report_soup = connect(latest_report_url)
    # latest_report_html = urllib2.urlopen(latest_report_url)
    # latest_report_soup = BeautifulSoup(latest_report_html)
    latest_report = ''
    try:
        latest_report = latest_report_soup.find('h2', text=re.compile('Reports')).find_next('div').text.strip()
    except:
        pass
    reports_url = ''
    try:
        reports_url = report_soup.find('div', 'overview-inner latest-report').find('li').find_next('li').find('a')['href']
    except:
        pass
    if 'pdf' not in reports_url:
        reports_url = ''
        try:
            if 'http' not in report_soup.find('a', text=re.compile('Read CQC inspection report online'))['href']:
                reports_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('Read CQC inspection report online'))['href']
            else:
                reports_url = report_soup.find('a', text=re.compile('Read CQC inspection report online'))['href']
        except:
            pass
    report_date = ''
    try:
        report_date = report_soup.find('div', 'overview-inner latest-report').find('h3').text.strip()
    except:
        pass
    overview = ''
    try:
        overview = report_soup.find('div', 'overview-inspections').find('h3').find('strong').text.strip()
    except:
        try:
            overview = report_soup.find('div', 'header-wrapper').find('h2').text.strip()
        except:
            pass
    overview_description = ''
    try:
        overview_description = report_soup.find('h3', 'accordion-title').find_next('div', 'accordion-wrapper').text.strip()
    except:
        pass
    overview_safe = ''
    try:
        overview_safe = report_soup.find('a', text=re.compile('\\bSafe\\b')).find_next('span').text.strip()
    except:
        pass
    overview_effective = ''
    try:
        overview_effective = report_soup.find('a', text=re.compile('\\bEffective\\b')).find_next('span').text.strip()
    except:
        pass
    overview_caring = ''
    try:
         overview_caring = report_soup.find('a', text=re.compile('\\bCaring\\b')).find_next('span').text.strip()
    except:
        pass
    overview_responsive = ''
    try:
        overview_responsive = report_soup.find('a', text=re.compile('Responsive')).find_next('span').text.strip()
    except:
        pass
    overview_well_led = ''
    try:
        overview_well_led = report_soup.find('a', text=re.compile('Well-led')).find_next('span').text.strip()
    except:
        pass
    run_by = ''
    try:
        run_by = report_soup.find('h3', text=re.compile('Who runs this service')).find_next('p').text.strip().split('run by')[-1]
    except:
        pass
    run_by_url = ''
    try:
        if 'http' not in report_soup.find('h3', text=re.compile('Who runs this service')).find_next('p').find('a')['href']:
            run_by_url = 'http://www.cqc.org.uk'+report_soup.find('h3', text=re.compile('Who runs this service')).find_next('p').find('a')['href']
        else:
            run_by_url = report_soup.find('h3', text=re.compile('Who runs this service')).find_next('p').find('a')['href']
    except:
        pass
    overview_summary_url = ''
    try:
        if 'http' not in report_soup.find('a', text=re.compile('Read overall summary'))['href']:
            overview_summary_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('Read overall summary'))['href']
        else:
            overview_summary_url = report_soup.find('a', text=re.compile('Read overall summary'))['href']
    except:
        pass
    overview_summary = ''
    if overview_summary_url:
        # overview_summary_page = urllib2.urlopen(overview_summary_url)
        # overview_summary_soup = BeautifulSoup(overview_summary_page, 'lxml')
        overview_summary_soup = connect(overview_summary_url)
        try:
            overview_summary = overview_summary_soup.find('h2', text=re.compile('Overall summary & rating')).find_next('div').text.strip()
        except:
            overview_summary = '
    summary_safe_url = ''
    try:
        if 'http' not in report_soup.find('a', text=re.compile('\\bSafe\\b'))['href']:
            summary_safe_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('\\bSafe\\b'))['href']
        else:
            summary_safe_url = report_soup.find('a', text=re.compile('\\bSafe\\b'))['href']
    except:
        pass
    summary_safe = ''
    if summary_safe_url and '#safe' in summary_safe_url:
        # summary_safe_page = urllib2.urlopen(summary_safe_url)
        # summary_safe_soup = BeautifulSoup(summary_safe_page, 'lxml')
        summary_safe_soup = connect(summary_safe_url)
        try:
            summary_safe = summary_safe_soup.find('h2', text=re.compile('\\bSafe\\b')).find_next('div').text.strip()
        except:
            summary_safe = ''
    summary_effective_url = ''
    try:
        if 'http' not in report_soup.find('a', text=re.compile('\\bEffective\\b'))['href']:
            summary_effective_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('\\bEffective\\b'))['href']
        else:
            summary_effective_url = report_soup.find('a', text=re.compile('\\bEffective\\b'))['href']
    except:
        pass
    # print summary_effective_url
    summary_effective = ''
    if summary_effective_url:
        # summary_effective_page = urllib2.urlopen(summary_effective_url)
        # summary_effective_soup = BeautifulSoup(summary_effective_page, 'lxml')
        summary_effective_soup =connect(summary_effective_url)
        try:
            summary_effective = summary_effective_soup.find('h2', text=re.compile('\\bEffective\\b')).find_next('div').text.strip()
        except:
            summary_effective = '
    summary_caring_url = ''
    try:
        caring_url_check = report_soup.find('a', text=re.compile('\\bCaring\\b'))['href']
        if '#caring' in caring_url_check:
            if 'http' not in report_soup.find('a', text=re.compile('\\bCaring\\b'))['href']:
                summary_caring_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('\\bCaring\\b'))['href']
            else:
                summary_caring_url = report_soup.find('a', text=re.compile('\\bCaring\\b'))['href']
    except:
        pass
    summary_caring = ''
    if summary_caring_url:
        # summary_caring_page = urllib2.urlopen(summary_caring_url)
        # summary_caring_soup = BeautifulSoup(summary_caring_page, 'lxml')
        summary_caring_soup = connect(summary_caring_url)
        try:
            summary_caring = summary_caring_soup.find('h2', text=re.compile('\\bCaring\\b')).find_next('div').text.strip()
        except:
             summary_caring = ''
    summary_responsive_url = ''
    try:
        if 'http' not in report_soup.find('a', text=re.compile('\\bResponsive\\b'))['href']:
            summary_responsive_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('\\bResponsive\\b'))['href']
        else:
            summary_responsive_url = report_soup.find('a', text=re.compile('\\bResponsive\\b'))['href']
    except:
        pass
    summary_responsive = ''
    if summary_responsive_url:
        # summary_responsive_page = urllib2.urlopen(summary_responsive_url)
        # summary_responsive_soup = BeautifulSoup(summary_responsive_page, 'lxml')
        summary_responsive_soup = connect(summary_responsive_url)
        summary_responsive = ''
        try:
            summary_responsive = summary_responsive_soup.find('h2', text=re.compile('\\bResponsive\\b')).find_next('div').text.strip()
        except:
            pass
    summary_well_led_url = ''
    try:
        if 'http' not in report_soup.find('a', text=re.compile('Well-led'))['href']:
            summary_well_led_url = 'http://www.cqc.org.uk'+report_soup.find('a', text=re.compile('Well-led'))['href']
        else:
            summary_well_led_url = report_soup.find('a', text=re.compile('Well-led'))['href']
    except:
        pass
    summary_well_led = ''
    if summary_well_led_url:
        summary_well_led_soup = connect(summary_well_led_url)
        try:
            summary_well_led = summary_well_led_soup.find('h2', text=re.compile('Well-led')).find_next('div').text.strip()
        except:
            summary_well_led = ''
    scraperwiki.sqlite.save(unique_keys=['location_url'], data={"location_url": unicode(location_url), "name": unicode(name), "add1": unicode(add1), "add2": unicode(add2), "add3": unicode(add3), "add4": unicode(add4), "postal_code": unicode(postal_code), "telephone": unicode(telephone),
                                                     "CQC_ID": cqc_id, "type_of_service": unicode(type_of_service), "services": unicode(services), "local_authority": unicode(local_authority), "latest_report": unicode(latest_report), "reports_url": unicode(reports_url),
                                                     "report_date": unicode(report_date), "overview": unicode(overview), "overview_description": unicode(overview_description), "overview_safe": unicode(overview_safe), "overview_effective": unicode(overview_effective),
                                                     "overview_caring": unicode(overview_caring), "overview_responsive": unicode(overview_responsive), "overview_well_led": unicode(overview_well_led), "run_by": unicode(run_by), "run_by_url": unicode(run_by_url),
                                                     "overview_summary": unicode(overview_summary), "summary_safe": unicode(summary_safe), "summary_effective": unicode(summary_effective), "summary_caring": unicode(summary_caring), "summary_responsive": unicode(summary_responsive),
                                                     "summary_well_led": unicode(summary_well_led)
                                                     })
    p+=1
