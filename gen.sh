echo '<!DOCTYPE html>' > adver.html
echo '<html lang="en">' >> adver.html
echo '<head>' >> adver.html
echo '    <meta charset="UTF-8">' >> adver.html
echo '    <meta http-equiv="X-UA-Compatible" content="IE=edge">' >> adver.html
echo '    <meta name="viewport" content="width=device-width, initial-scale=1.0">' >> adver.html
echo '    <title>Document</title>' >> adver.html
echo '</head>' >> adver.html
echo '<body>' >> adver.html
echo '    <div id="main" style="margin: 50px; width: min-content;">' >> adver.html
echo '        @@' >> adver.html
echo '    </div>' >> adver.html
echo '</body>' >> adver.html
echo '<style>' >> adver.html
echo '' >> adver.html
echo '    body, #main {' >> adver.html
echo '        width: 99%;' >> adver.html
echo '        height: 100%;' >> adver.html
echo '        display: flex;' >> adver.html
echo '        flex-direction: column;' >> adver.html
echo '        align-content: center;' >> adver.html
echo '        justify-content: center;' >> adver.html
echo '        background: white;' >> adver.html
echo '    }' >> adver.html
echo '</style>' >> adver.html
echo '</html>"' >> adver.html
python3 test_scraper.py
python3 assembler.py