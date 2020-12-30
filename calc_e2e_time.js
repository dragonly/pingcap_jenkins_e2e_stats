const fs = require('fs');
const puppeteer = require('puppeteer');

const DATA_DIR = 'e2e_time_data'

async function extractPageContent(page) {
  const startTime = await page.evaluate(() => {
    let timeElems = document.querySelectorAll('.RunDetailsHeader-times div')
    let durationStr = timeElems[0].querySelector('span').innerText
    let duration = parseDurationToSeconds(durationStr)
    let startTimeStr = timeElems[1].querySelector('time').getAttribute('datetime')
    let startTimestamp = Date.parse(startTimeStr)
    return { durationStr, duration, startTimestamp, startTimeStr }
  })

  const failedTests = await page.evaluate(() => (
    [...document.querySelectorAll('.result-item.failure')].map(extractTest)
  ));

  const skippedTests = await page.evaluate(() => (
    [...document.querySelectorAll('.result-item.not_built')].map(extractTest)
  ));

  const passedTests = await page.evaluate(() => (
    [...document.querySelectorAll('.result-item.success')].map(extractTest)
  ));

  return {
    startTime,
    failedTests,
    skippedTests,
    passedTests
  }
}

async function extractPage(page, jobNum) {
  const url = `https://internal.pingcap.net/idc-jenkins/blue/organizations/jenkins/tidb-operator-pull-e2e-kind/detail/tidb-operator-pull-e2e-kind/${jobNum}/tests/`
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  try {
    await page.waitForSelector('.result-item', { timeout: 10000 })
  } catch {
    console.log('wait for .result-item element in page timeout, skip')
    return
  }
  // setup global helper functions in page js context, which is not in this nodejs context
  await page.evaluate(() => {
    window.extractTest = (elem) => {
      return {
        name: elem.querySelector('.result-item-label').innerText,
        durationStr: elem.querySelector('.result-item-extra-info').innerText,
        duration: parseDurationToSeconds(elem.querySelector('.result-item-extra-info').innerText)
      }
    }
    window.parseDurationToSeconds = (duration) => {
      if (duration === '<1s') {
        return 1
      }
      hms = duration.split(' ')
      sec = 0
      len = hms.length
      // hms.forEach(i => console.log(i))
      if (len > 0) {
        s = hms[len - 1]
        if (!s.endsWith('s')) {
          return -1
        }
        sec += parseInt(s)
      }
      if (len > 1) {
        m = hms[len - 2]
        if (!m.endsWith('m')) {
          return -2
        }
        sec += parseInt(m) * 60
      }
      if (len > 2) {
        h = hms[len - 3]
        if (!h.endsWith('h')) {
          return -3
        }
        sec += parseInt(h) * 3600
      }
      if (len > 3) {
        return -4
      }
      return sec
    }
  });

  console.log(url);
  page.on('console', msg => {
    console.log(msg.text())
  });
  let pageContent = await extractPageContent(page)
  await fs.writeFileSync(`${DATA_DIR}/${jobNum}.json`, JSON.stringify(pageContent, null, 2))
}

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  for (let jobNum = 1; jobNum < 3650; jobNum++) {
    console.log(`start extracting job ${jobNum}`)
    await extractPage(page, jobNum)
    console.log(`finish extracting job ${jobNum}`)
  }

  await browser.close();
})();
