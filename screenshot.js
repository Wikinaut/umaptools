const puppeteer = require('puppeteer');         // Require Puppeteer module
const myArgs = process.argv.slice(2);

# based on https://www.testim.io/blog/puppeteer-screenshot/

if (myArgs.length < 1) {

   console.log("Usage: node screenshot.js umapnumber [width height imageoutputfile]")
   // const url = "https://umap.openstreetmap.fr/de/map/__720091#19/52.47720/13.3310"; // Set website you want to screenshot
   return

} else if (myArgs.length == 1) {

   url = myArgs[0]
   userwidth = 2500;
   userheight = 2250;
   outfile = "./screenshot.png";

} else {

  url = myArgs[0];
  userwidth = parseInt(myArgs[1],10);
  userheight = parseInt(myArgs[2],10);
  outfile = ( myArgs.length == 4 ) ? myArgs[3] : "./screenshot.png";

}

const Screenshot = async () => {                // Define Screenshot function

   const browser = await puppeteer.launch({headless:true,slowMo: 50 });    // Launch a "browser"

   const page = await browser.newPage();        // Open a new page

   await page.setViewport({
     width: userwidth,
     height: userheight,
     deviceScaleFactor: 1.0,
   });

   await page.goto(url);                        // Go to the website

   await page.screenshot({                      // Screenshot the website using defined options
    path: outfile,                   // Save the screenshot in current directory
    fullPage: true                              // take a fullpage screenshot
  });

  await page.close();                           // Close the website
  await browser.close();                        // Close the browser
}

Screenshot();                                   // Call the Screenshot function
