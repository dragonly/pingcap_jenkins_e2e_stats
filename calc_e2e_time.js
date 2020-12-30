const puppeteer = require('puppeteer');

async function extractPageContent(page) {
  const failedTests = await page.evaluate(() => (
    [...document.querySelectorAll('.result-item.failure')].map(elem => ({
      title: elem.querySelector('.result-item-label').innerText,
      time: elem.querySelector('.result-item-extra-info').innerText,
    }))
  ));

  const skippedTests = await page.evaluate(() => (
    [...document.querySelectorAll('.result-item.not_built')].map(elem => ({
      title: elem.querySelector('.result-item-label').innerText,
      time: elem.querySelector('.result-item-extra-info').innerText,
    }))
  ));

  const passedTests = await page.evaluate(() => (
    [...document.querySelectorAll('.result-item.success')].map(elem => ({
      title: elem.querySelector('.result-item-label').innerText,
      time: elem.querySelector('.result-item-extra-info').innerText,
    }))
  ));

  return {
    failedTests,
    skippedTests,
    passedTests
  }
}

async function extractPage(browser, url) {
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('.test-result-block.new-failure-block .result-item')
  console.log(url);
  console.log(await extractPageContent(page))
}

(async () => {
  const browser = await puppeteer.launch();
  
  const jobNum = 3633
  let url = `https://internal.pingcap.net/idc-jenkins/blue/organizations/jenkins/tidb-operator-pull-e2e-kind/detail/tidb-operator-pull-e2e-kind/${jobNum}/tests/`
  await extractPage(browser, url)

  await browser.close();
})();
