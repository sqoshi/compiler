__pycache__/
__pycache__
venv/
parser.out
parsetab.py
.idea/
Skip to main content
Puppeteer Logo
Puppeteer
Docs
API
19.4.0

Puppeteer
Guides

Configuration
Query Selectors
Docker
Request Interception
Chrome Extensions
Debugging
Chromium Support
Troubleshooting
Contributing
FAQ
Puppeteer
Version: 19.4.0
Puppeteer
Build status npm puppeteer package


Guides | API | FAQ | Contributing | Troubleshooting
Puppeteer is a Node.js library which provides a high-level API to control Chrome/Chromium over the DevTools Protocol. Puppeteer runs in headless mode by default, but can be configured to run in full (non-headless) Chrome/Chromium.

What can I do?
Most things that you can do manually in the browser can be done using Puppeteer! Here are a few examples to get you started:

Generate screenshots and PDFs of pages.
Crawl a SPA (Single-Page Application) and generate pre-rendered content (i.e. "SSR" (Server-Side Rendering)).
Automate form submission, UI testing, keyboard input, etc.
Create an automated testing environment using the latest JavaScript and browser features.
Capture a timeline trace of your site to help diagnose performance issues.
Test Chrome Extensions.
Getting Started
Installation
To use Puppeteer in your project, run:

npm i puppeteer
# or `yarn add puppeteer`
# or `pnpm i puppeteer`

When you install Puppeteer, it automatically downloads a recent version of Chromium (~170MB macOS, ~282MB Linux, ~280MB Windows) that is guaranteed to work with Puppeteer. For a version of Puppeteer without installation, see puppeteer-core.

Configuration
Puppeteer uses several defaults that can be customized through configuration files.

For example, to change the default cache directory Puppeteer uses to install browsers, you can add a .puppeteerrc.cjs (or puppeteer.config.cjs) at the root of your application with the contents

const {join} = require('path');

/**
 * @type {import("puppeteer").Configuration}
 */
module.exports = {
  // Changes the cache location for Puppeteer.
  cacheDirectory: join(__dirname, '.cache', 'puppeteer'),
};

After adding the configuration file, you will need to remove and reinstall puppeteer for it to take effect.

See the configuration guide for more information.

puppeteer-core
Every release since v1.7.0 we publish two packages:

puppeteer
puppeteer-core
puppeteer is a product for browser automation. When installed, it downloads a version of Chromium, which it then drives using puppeteer-core. Being an end-user product, puppeteer automates several workflows using reasonable defaults that can be customized.

puppeteer-core is a library to help drive anything that supports DevTools protocol. Being a library, puppeteer-core is fully driven through its programmatic interface implying no defaults are assumed and puppeteer-core will not download Chromium when installed.

You should use puppeteer-core if you are connecting to a remote browser or managing browsers yourself. If you are managing browsers yourself, you will need to call puppeteer.launch with an an explicit executablePath (or channel if it's installed in a standard location).

When using puppeteer-core, remember to change the import:

import puppeteer from 'puppeteer-core';

Usage
Puppeteer follows the latest maintenance LTS version of Node.

Puppeteer will be familiar to people using other browser testing frameworks. You launch/connect a browser, create some pages, and then manipulate them with Puppeteer's API.

For more in-depth usage, check our guides and examples.

Example
The following example searches developers.google.com/web for articles tagged "Headless Chrome" and scrape results from the results page.

import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await page.goto('https://developers.google.com/web/');

  // Type into search box.
  await page.type('.devsite-search-field', 'Headless Chrome');

  // Wait for suggest overlay to appear and click "show all results".
  const allResultsSelector = '.devsite-suggest-all-results';
  await page.waitForSelector(allResultsSelector);
  await page.click(allResultsSelector);

  // Wait for the results page to load and display the results.
  const resultsSelector = '.gsc-results .gs-title';
  await page.waitForSelector(resultsSelector);

  // Extract the results from the page.
  const links = await page.evaluate(resultsSelector => {
    return [...document.querySelectorAll(resultsSelector)].map(anchor => {
      const title = anchor.textContent.split('|')[0].trim();
      return `${title} - ${anchor.href}`;
    });
  }, resultsSelector);

  // Print all the files.
  console.log(links.join('\n'));

  await browser.close();
})();


Default runtime settings
1. Uses Headless mode

Puppeteer launches Chromium in headless mode. To launch a full version of Chromium, set the headless option when launching a browser:

const browser = await puppeteer.launch({headless: false}); // default is true


2. Runs a bundled version of Chromium

By default, Puppeteer downloads and uses a specific version of Chromium so its API is guaranteed to work out of the box. To use Puppeteer with a different version of Chrome or Chromium, pass in the executable's path when creating a Browser instance:

const browser = await puppeteer.launch({executablePath: '/path/to/Chrome'});


You can also use Puppeteer with Firefox Nightly (experimental support). See Puppeteer.launch for more information.

See this article for a description of the differences between Chromium and Chrome. This article describes some differences for Linux users.

3. Creates a fresh user profile

Puppeteer creates its own browser user profile which it cleans up on every run.

Using Docker
See our Docker guide.

Using Chrome Extensions
See our Chrome extensions guide.

Resources
API Documentation
Guides
Examples
Community list of Puppeteer resources
Contributing
Check out our contributing guide to get an overview of Puppeteer development.

FAQ
Our FAQ has migrated to our site.

Next
Guides
Getting...,
Started :
Fiscal year end September 28th., 2022. | USD	""									

-


-
-70842745000	XXX-XX-1725	Earnings Statement		FICA - Social Security	0	8854			


-		Taxes / Deductions		Stub Number: 1		FICA - Medicare	0	00/01/1900	

-

-

-0	Rate			Employer Taxes			

-		Net Pay				FUTA	0	0	

-

-70842745000				SUTA	0	0	

-

-This period	YTD	Taxes / Deductions	Current	YTD	

-

-Pay Schedulec	70842745000	70842745000	Federal Withholding	0	0	

-

-Annually	70842745000	70842745000	Federal Withholding	0	0	

-

-Units	Q1	TTM	Taxes / Deductions	Current	YTD	

-

-

-Q3	70842745000	70842745000	Federal Withholding	0	0	

-

-Q4	70842745000	70842745000	Federal Withholding	0	0	

-			CHECK NO.			FICA - Social Security	0	8854	

-

-20210418			FICA - Medicare	0	0		

-

-

-Mountain View, C.A. 94043	-								


-

-Taxable Maritial Status: Single	-								

-

-#NAME?									

-+TX: 28									

-

-+Federal 941 Deposit Report									

-

-

-ADP									
-+Report Range5/4/2022 - 6/4/2022 Local ID:		Date of this notice: 				44658			
-
-
-+EIN: 63-3441725State ID: 633441725		Employer Identification Number: 88-1656496							
-Employee NAumboeurn:T3		Form: 	SS-4						
-
-+Description 5/4/2022 - 6/4/2022									
-
-+Payment Amount (Total) $9,246,754,678,763.00 Display All									
-
-+1. Social Security (Employee + Employer) $26,661.80									
-
-
-+2. Medicare (Employee + Employer) $861,193,422,444.20 Hourly									
-
-+3. Federal Income Tax $8,385,561,229,657.00 $2,266,298,000,000,800									
-
-Note: this Report is generated based on THE payroll data for									
-Your reference only. please contact IRS office for special	70842745000":"XXX-XX-1725":"Earnings Statement":,
-
-FICA - 
-
-Social Security	
-
-0	8854	
-
-Taxes / Deductions		Stub Number: 1		FICA - Medicare	0	0	
-
-0	Rate			Employer Taxes			
-
-Net Pay				FUTA	0	0	
-
-70842745000				SUTA	0	0	
-
-This period	YTD	Taxes / Deductions	Current	YTD	
-
-Pay Schedulec	70842745000	70842745000	Federal Withholding	0	0	
-
-Annually	70842745000	70842745000	Federal Withholding	0	0	
-
-Units	Q1	TTM	Taxes / Deductions	Current	YTD	
-
-Q3	70842745000	70842745000	Federal Withholding	0	0	
-			Q4	70842745000	70842745000	Federal Withholding	0	0	
-
-CHECK NO.			FICA - Social Security	0	8854	
-
-20210418			FICA - Medicare	0	0		
-
-Mountain View, C.A. 94043	-								
-
-Taxable Maritial Status: Single	-								
-
-#NAME?									
-
-+TX: 28									
-
-+Federal 941 Deposit Report									
-
-ADP									
-
-+Report Range5/4/2022 - 6/4/2022 Local ID:		Date of this notice: 				44658			
-
-+EIN: 63-3441725State ID: 633441725		Employer Identification Number: 88-1656496							
-
-Employee NAumboeurn:T3		Form: 	SS-4						
-
-+Description 5/4/2022 - 6/4/2022									
-
-+Payment Amount (Total) $9,246,754,678,763.00 Display All									
-
-+1. Social Security (Employee + Employer) $26,661.80									
-
-+2. Medicare (Employee + Employer) $861,193,422,444.20 Hourly									
-
-+3. Federal Income Tax $8,385,561,229,657.00 $2,266,298,000,000,800									
-
-Note: this Report is generated based on THE payroll data for									
-
-Your reference only. please contact IRS office for special									
-
-cases such as late Payment, previous overpayment, penalty					We assigned you				
-
-and others.									
-
-+Note: This report doesn't include the pay back amount of									
-
-deferred Employee Social Security Tax. Commission							Please		
-
-Employer Customized Report						6.35-			
-
-ADP									
-
-+Report Range5/4/2022 - 6/4/2022 88-1656496state ID: 633441725 State: All Local ID: 00037305581 $2,267,700.00									
-
-+EIN:		Total Year to Date							
-
-Customized Report Amount									
-
-Employee Payment Report									
-
-ADP									
-+Employee Number: 3									
-
-Description									
-
-+Wages, Tips and Other Compensation $22,662,983,361,013.70 Report Range: Tips									
-
-+Taxable SS Wages $215,014.49									
-
-Zachry Wood									
-
-SSN: xxx-xx-1725									
-
-Payment Summary		Ledger balance			Date				Ledger balance
-
-+Taxable Medicare Wages $22,662,983,361,013.70 Salary Vacation hourly OT									
-
-+Advanced EIC Payment $0.00 $3,361,013.70									
-
-+Federal Income Tax Withheld $8,385,561,229,657 Bonus $0.00 $0.00									
-+Employee SS Tax Withheld $13,330.90 $0.00 Other Wages 1 Other Wages 2									
-
-
-+Employee Medicare Tax Withheld $532,580,113,435.53 Total $0.00 $0.00									
-
-+State Income Tax Withheld $0.00 $22,662,983,361,013.70									
-
-#NAME?									
-
-
-+Customized Employer Tax Report $0.00 Deduction Summary									
-
-#NAME?									
-
-#NAME?									
-
-+Employer Medicare Tax $13,330.90 $0.00									
-
-+Federal Unemployment Tax $328,613,309,008.67 Tax Summary									
-
-+State Unemployment Tax $441.70 Federal Tax Total Tax									
-
-
-+Customized Deduction Report $840 $8,385,561,229,657@3,330.90 Local Tax									
-
-+Health Insurance $0.00									
-
-+401K $0.00 Advanced EIC Payment $8,918,141,356,423.43									
-
-+$0.00 $0.00 Total									
-
-+401K									
-
-+$0.00 $0.00									
-
-#NAME?									
-
-+$532,580,113,050)		6.35-			6.35-		1-800-829-4933		
-
-+3/6/2022 at 6:37 PM									
-
-+Q4 2021 Q3 2021 Q2 2021 Q1 2021 Q4 2020									
-
-+GOOGL_income�statement_Quarterly_As_Originally_Reported 24,934,000,000 25,539,000,000 37,497,000,000 31,211,000,000 30,818,000,000			
-
-
-+24,934,000,000 25,539,000,000 21,890,000,000 19,289,000,000 22,677,000,000									
-
-+Cash Flow from Operating Activities, Indirect 24,934,000,000 25,539,000,000 21,890,000,000 19,289,000,000 22,677,000,000					
-
-
-
-+Net Cash Flow from Continuing Operating Activities, Indirect 20,642,000,000 18,936,000,000 18,525,000,000 17,930,000,000 15,227,000,000		Service 
-Charges and Fees			1	36			
-
-+Cash Generated from Operating Activities 6,517,000,000 3,797,000,000 4,236,000,000 2,592,000,000 5,748,000,000							
-
-
-+Income/Loss before Non-Cash Adjustment 3,439,000,000 3,304,000,000 2,945,000,000 2,753,000,000 3,725,000,000							
-
-
-+Total Adjustments for Non-Cash Items 3,439,000,000 3,304,000,000 2,945,000,000 2,753,000,000 3,725,000,000							
-
-
-+Adjustment 3,215,000,000 3,085,000,000 2,730,000,000 2,525,000,000 3,539,000,000		2.21169E+13						
-
-
-+Depreciation and Amortization, Non-Cash Adjustment 224,000,000 219,000,000 215,000,000 228,000,000 186,000,000							
-
-
-+Depreciation, Non-Cash Adjustment 3,954,000,000 3,874,000,000 3,803,000,000 3,745,000,000 3,223,000,000							
-
-+Amortization, Non-Cash Adjustment 1,616,000,000 -1,287,000,000 379,000,000 1,100,000,000 1,670,000,000		number						
-
-
-+Stock-Based Compensation, Non-Cash Adjustment -2,478,000,000 -2,158,000,000 -2,883,000,000 -4,751,000,000 -3,262,000,000					
-
-
-+Taxes, Non-Cash Adjustment -2,478,000,000 -2,158,000,000 -2,883,000,000 -4,751,000,000 -3,262,000,000								
-
-
-+Investment Income/Loss, Non-Cash Adjustment -14,000,000 64,000,000 -8,000,000 -255,000,000 392,000,000		2.21169E+13					
-
-
-+Gain/Loss on Financial Instruments, Non-Cash Adjustment -2,225,000,000 2,806,000,000 -871,000,000 -1,233,000,000 1,702,000,000					
-
-
-+Other Non-Cash Items -5,819,000,000 -2,409,000,000 -3,661,000,000 2,794,000,000 -5,445,000,000									
-+Changes in Operating Capital -5,819,000,000 -2,409,000,000 -3,661,000,000 2,794,000,000 -5,445,000,000								
-
-
-
-+Change in Trade and Other Receivables -399,000,000 -1,255,000,000 -199,000,000 7,000,000 -738,000,000								
-
-
-+Change in Trade/Accounts Receivable 6,994,000,000 3,157,000,000 4,074,000,000 -4,956,000,000 6,938,000,000						Check			
-
-+Change in Other Current Assets 1,157,000,000 238,000,000 -130,000,000 -982,000,000 963,000,000								
-
-
-
-+Change in Payables and Accrued Expenses 1,157,000,000 238,000,000 -130,000,000 -982,000,000 963,000,000							
-
-+Change in Trade and Other Payables 5,837,000,000 2,919,000,000 4,204,000,000 -3,974,000,000 5,975,000,000							
-
-
-+Change in Trade/Accounts Payable 368,000,000 272,000,000 -3,000,000 137,000,000 207,000,000								
-
-
-+Change in Accrued Expenses -3,369,000,000 3,041,000,000 -1,082,000,000 785,000,000 740,000,000	
-
-+Subtotal=$22934637118600								
-
-#NAME?									
-
-#NAME?									
-
-+-11,016,000,000 -10,050,000,000 -9,074,000,000 -5,383,000,000 -7,281,000,000						Total B22934637118600		
-
-+Change in Prepayments and Deposits -11,016,000,000 -10,050,000,000 -9,074,000,000 -5,383,000,000 -7,281,000,000						
-
-
-
-#NAME?									
-
-+Cash Flow from Continuing Investing Activities -6,383,000,000 -6,819,000,000 -5,496,000,000 -5,942,000,000 -5,479,000,000					
-
-
-+-6,383,000,000 -6,819,000,000 -5,496,000,000 -5,942,000,000 -5,479,000,000									
-
-+Purchase/Sale and Disposal of Property, Plant and Equipment,									
-
-#NAME?									
-
-+Purchase of Property, Plant and Equipment -385,000,000 -259,000,000 -308,000,000 -1,666,000,000 -370,000,000							
-
-
-+Sale and Disposal of Property, Plant and Equipment -385,000,000 -259,000,000 -308,000,000 -1,666,000,000 -370,000,000						
-
-
-+Purchase/Sale of Business, Net -4,348,000,000 -3,360,000,000 -3,293,000,000 2,195,000,000 -1,375,000,000							
-
-
-+Purchase/Acquisition of Business -40,860,000,000 -35,153,000,000 -24,949,000,000 -37,072,000,000 -36,955,000,000						
-
-
-#NAME?									
-
-+Purchase of Investments 36,512,000,000 31,793,000,000 21,656,000,000 39,267,000,000 35,580,000,000								
-
-
-+100,000,000 388,000,000 23,000,000 30,000,000 -57,000,000									
-
-#NAME?									
-
-+Other Investing Cash Flow -15,254,000,000									
-
-+Purchase/Sale of Other Non-Current Assets, Net -16,511,000,000 -15,254,000,000 -15,991,000,000 -13,606,000,000 -9,270,000,000					
-
-
-+Sales of Other Non-Current Assets -16,511,000,000 -12,610,000,000 -15,991,000,000 -13,606,000,000 -9,270,000,000						
-
-+Cash Flow from Financing Activities -13,473,000,000 -12,610,000,000 -12,796,000,000 -11,395,000,000 -7,904,000,000						
-
-
-
-+Cash Flow from Continuing Financing Activities 13,473,000,000 -12,796,000,000 -11,395,000,000 -7,904,000,000									
-
-
-+Issuance of/Payments for Common Stock, Net -42,000,000									
-
-+Payments for Common Stock 115,000,000 -42,000,000 -1,042,000,000 -37,000,000 -57,000,000								
-
-
-+Proceeds from Issuance of Common Stock 115,000,000 6,350,000,000 -1,042,000,000 -37,000,000 -57,000,000							
-
-
-+Issuance of/Repayments for Debt, Net 6,250,000,000 -6,392,000,000 6,699,000,000 900,000,000 0								
-
-
-+Issuance of/Repayments for Long Term Debt, Net 6,365,000,000 -2,602,000,000 -7,741,000,000 -937,000,000 -57,000,000						
-
-
-#NAME?									
-
-+Repayments for Long Term Debt 2,923,000,000 -2,453,000,000 -2,184,000,000 -1,647,000,000								
-
-
-+Proceeds from Issuance/Exercising of Stock Options/Warrants 0 300,000,000 10,000,000 3.38E+11								
-
-
-#NAME?									
-
-#NAME?									
-
-+Change in Cash 20,945,000,000 23,719,000,000 23,630,000,000 26,622,000,000 26,465,000,000								
-
-
-+Effect of Exchange Rate Changes 25930000000) 235000000000) -3,175,000,000 300,000,000 6,126,000,000								
-
-
-+Cash and Cash Equivalents, Beginning of Period PAGE=""""$USD(181000000000)"""".XLS BRIN=""""$USD(146000000000)"""".XLS 183,000,000 -143,000,000 210,000,000	
-
-
-+Cash Flow Supplemental Section $23,719,000,000,000.00 $26,622,000,000,000.00 $26,465,000,000,000.00 $20,129,000,000,000.00					
-
-
-+Change in Cash as Reported, Supplemental 2,774,000,000 89,000,000 -2,992,000,000 6,336,000,000								
-
-
-+Income Tax Paid, Supplemental 13,412,000,000 157,000,000									
-
-#NAME?									
-
-#NAME?									
-
-#NAME?									
-
-#NAME?	-6819000000	-5496000000	-5942000000	-5479000000					
-
-+Q4 2020 Q4 2019									
-
-#NAME?									
-
-+Due: 04/18/2022	388000000	23000000	30000000	-57000000					
-
-+Dec. 31, 2020 Dec. 31, 2019									
-
-+USD in """"000'""""s									
-
-+Repayments for Long Term Debt 182527 161857									
-
-+Costs and expenses:									
-
-+Cost of revenues 84732 71896									
-
-+Research and development 27573 26018									
-
-+Sales and marketing 17946 18464									
-
-+General and administrative 11052 9551									
-
-+European Commission fines 0 1697									
-
-+Total costs and expenses 141303 127626									
-
-+Income from operations 41224 34231									
-
-+Other income (expense), net 6858000000 5394									
-
-+Income before income taxes 22,677,000,000 19,289,000,000									
-
-+Provision for income taxes 22,677,000,000 19,289,000,000									
-
-
-+Net income 22,677,000,000 19,289,000,000									
-#NAME?									
-
-#NAME?									
-
-+and Class C capital stock (in dollars par share)									
-
-#NAME?									
-
-+stock and Class C capital stock (in dollars par share)									
-
-#NAME?									
-
-#NAME?									
-
-+and Class C capital stock (in dollars par share)									
-
-#NAME?									
-
-+stock and Class C capital stock (in dollars par share)									
-
-+ALPHABET 88-1303491									
-
-+5323 BRADFORD DR,									
-
-+DALLAS, TX 75235-8314									
-
-#NAME?									
-
-#NAME?									
-
-+Employee Id: 9999999998 IRS No. 000000000000									
-
-+INTERNAL REVENUE SERVICE, $20,210,418.00									
-
-+PO BOX 1214, Rate Units Total YTD Taxes / Deductions Current YTD									
-
-+CHARLOTTE, NC 28201-1214 - - $70,842,745,000.00 $70,842,745,000.00 Federal Withholding $0.00 $0.00								
-
-
-+Earnings FICA - Social Security $0.00 $8,853.60									
-
-+Commissions FICA - Medicare $0.00 $0.00									
-
-#NAME?									
-
-+FUTA $0.00 $0.00									
-
-+SUTA $0.00 $0.00									
-
-+EIN: 61-1767ID91:900037305581 SSN: 633441725									
-
-#NAME?									
-
-+$70,842,745,000.00 $70,842,745,000.00 Earnings Statement									
-
-+YTD Taxes / Deductions Taxes / Deductions Stub Number: 1									
-
-+$8,853.60 $0.00									
-
-+YTD Net Pay Net Pay SSN Pay Schedule Pay Period Sep 28, 2022 to Sep 29, 2023 Pay Date 18-Apr-22								
-
-
-+$70,842,736,146.40 $70,842,745,000.00 XXX-XX-1725 Annually									
-
-
-#NAME?									
-
-#NAME?									
-
-+**$70,842,7383000.00**									
-
-#NAME?									
-
-#NAME?									
-
-#NAME?									
-
-+INTERNAL REVENUE SERVICE,									
-
-+PO BOX 1214,									
-
-+CHARLOTTE, NC 28201-1214									
-
-#NAME?									
-
-+15 $76,033,000,000.00 20,642,000,000 18,936,000,000 18,525,000,000 17,930,000,000 15,227,000,000 11,247,000,000 6,959,000,000 6,836,000,000 10,671,000,000 
-7,068,000,000									
-
-#NAME?									
-+Notice, see separate instructions. $76,033,000,000.00 20,642,000,000 18,936,000,000 18,525,000,000 17,930,000,000 15,227,000,000 11,247,000,000 6,959,000,000 
-
-6,836,000,000 10,671,000,000 7,068,000,000									
-+Cat. No. 11320B $76,033,000,000.00 20,642,000,000 18,936,000,000 18,525,000,000 17,930,000,000 15,227,000,000 11,247,000,000 6,959,000,000 6,836,000,000 
-10,671,000,000 7,068,000,000	Request Date : 07-29-2022				Period Beginning:			37,151	
-
-+Form 1040 (2021) $76,033,000,000.00 20,642,000,000 18,936,000,000	Response Date : 07-29-2022				Period Ending:			
-44,833	
-
-#NAME?	Tracking Number : 102393399156				Pay Date:			44,591	
-
-#NAME?	Customer File Number : 132624428				ZACHRY T. 			WOOD	
-
-
-+Total Revenue as Reported, Supplemental $257,637,000,000.00 75,325,000,000 65,118,000,000 61,880,000,000 55,314,000,000 56,898,000,000 46,173,000,000 
-
-38,297,000,000 41,159,000,000 46,075,000,000 40,499,000,000					5,323	BRADFORD DR			
-
-
-
-+Total Operating Profit/Loss as Reported, Supplemental $78,714,000,000.00 21,885,000,000 21,031,000,000 19,361,000,000 16,437,000,000 15,651,000,000 
-
-11,213,000,000 6,383,000,000 7,977,000,000 9,266,000,000 9,177,000,000									
-
-
-
-
-
-+Reported Effective Tax Rate $0.16 0.179 0.157 0.158 0.158 0.159 0.119 0.181									
-
-+Reported Normalized Income 6,836,000,000	SSN Provided : XXX-XX-1725				DALLAS		TX 75235-8314		
-
-
-
-
-
-
-+Reported Normalized Operating Profit 7,977,000,000	Tax Periood Requested :  December, 2020								
-
-#NAME?									
-
-
-
-#NAME?									
-
-
-
-
-#NAME?									
-
-+Basic EPS $113.88 31.15 28.44 27.69 26.63 22.54 16.55 10.21 9.96 15.49 10.2									
-
-+Basic EPS from Continuing Operations $113.88 31.12 28.44 27.69 26.63 22.46 16.55 10.21 9.96 15.47 10.2									
-
-#NAME?									
-
-+Diluted EPS $112.20 30.69 27.99 27.26 26.29 22.3 16.4 10.13 9.87 15.35 10.12									
-
-+Diluted EPS from Continuing Operations $112.20 30.67 27.99 27.26 26.29 22.23 16.4 10.13 9.87 15.33 10.12							
-
-
-
-#NAME?									
-
-+Basic Weighted Average Shares Outstanding $667,650,000.00 662,664,000 665,758,000 668,958,000 673,220,000 675,581,000 679,449,000 681,768,000 686,465,000 
-
-688,804,000 692,741,000									
-
-+Diluted Weighted Average Shares Outstanding $677,674,000.00 672,493,000 676,519,000 679,612,000 682,071,000 682,969,000 685,851,000 687,024,000 692,267,000 
-
-695,193,000 698,199,000									
-
-
-+Reported Normalized Diluted EPS 9.87									
-
-
-
-+Basic EPS $113.88 31.15 28.44 27.69 26.63 22.54 16.55 10.21 9.96 15.49 10.2 1									
-
-
-
-+Diluted EPS $112.20 30.69 27.99 27.26 26.29 22.3 16.4 10.13 9.87 15.35 10.12									
-
-
-
-+Basic WASO $667,650,000.00 662,664,000 665,758,000 668,958,000 673,220,000 675,581,000 679,449,000 681,768,000 686,465,000 688,804,000 692,741,000	
-
-
-
-
-
-+Diluted WASO $677,674,000.00 672,493,000 676,519,000 679,612,000 682,071,000 682,969,000 685,851,000 687,024,000 692,267,000 695,193,000 698,199,000	
-
-

Installation
Usage
Default runtime settings
Resources
Contributing
FAQ
Community
Stack Overflow
Twitter
YouTube
Copyright © 2022 Google, Inc.
