with open('templates/index.html', encoding='utf-8') as f:
    content = f.read()

old = '<div class="form-group"><label>EMAIL ADDRESS</label><input type="email" id="invsign-email" placeholder="you@institution.com"/></div>'
new = '<div class="form-group"><label>FULL NAME</label><input type="text" id="invsign-name" placeholder="Jane Smith"/></div>\n      ' + old

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content.replace(old, new, 1))

print('Done')