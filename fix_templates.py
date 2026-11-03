import re
files = ['templates/index.html', 'templates/settings.html']
pattern = re.compile(r"{%.*?if\s+current_user\.role\s*==\s*['\"]admin['\"]\s*%}\s*Unlimited\s*{%\s*else\s*%}\s*{{\s*current_user\.credits\s*}}\s*Credits\s*{%\s*endif\s*%}", re.DOTALL)
replacement = "{% if current_user.is_unlimited or current_user.role == 'admin' %}Unlimited{% else %}{{ current_user.credits }} Credits{% endif %}"
for file in files:
    try:
        with open(file, 'r') as f:
            content = f.read()
        if 'is_unlimited or' not in content:
            new_content = pattern.sub(replacement, content)
            if new_content != content:
                with open(file, 'w') as f:
                    f.write(new_content)
                print(f"✅ Updated {file}")
            else:
                print(f"⚠️ Could not find the exact text to replace in {file}.")
        else:
            print(f"✅ {file} already has the logic.")
    except Exception as e:
        print(f"Error with {file}: {e}")
