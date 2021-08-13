# Papers Bibtex Catcher
Here is the bibtex catcher that catch the bibtex of papers from IEEE and Google Scholar. 
It will first try IEEE and then Google Scholar. 
After catching the bibtex, it will generate a `bib` file that can be added to your paper reference files.

## Requirements
First, you need to install [Chrome](https://www.google.com/chrome/).

And then you should install the [chromedriver](https://chromedriver.chromium.org/downloads) according to the version of Chrome.

Config the paths in the Python Script.
```Python
# The path of Chrome driver
driver_path = r"${your_path}\chromedriver.exe"
# The data path of Chrome
option_path = r"C:\Users\${UserName}\AppData\Local\Google\Chrome\User Data"
```
Finally, install the dependency.
```
conda install selenium
```

Enjoy!
