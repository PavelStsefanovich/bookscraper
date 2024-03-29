$ErrorActionPreference = 'Stop'

$current_location = $PWD.Path
cd $PSScriptRoot

try {
    gi dist -ErrorAction SilentlyContinue | rm -Force -recurse
    # & pipenv install
    & pipenv run pyinstaller -F -i config/bookscraper.ico -n BookScraper main.py
    cp params.yml dist
    cp config dist -recurse
    rm dist/config/*.ico    
}
catch {
    throw $_
}
finally {
    write "BUILD FINISHED"
    cd $current_location
}
