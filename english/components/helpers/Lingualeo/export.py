from components.Resources import Resources
import handler
import service
import sys

settings = Resources.Settings('Lingualeo')

email = settings["email"]
password = settings["password"]


if export_type == 'text':
    word_handler = handler.Text(config.sources.get('text'))
elif export_type == 'kindle':
    word_handler = handler.Kindle(config.sources.get('kindle'))
else:
    raise Exception('unsupported type')

word_handler.read()

lingualeo = service.Lingualeo(email, password)
lingualeo.auth()
translate = lingualeo.get_translates('already')


if translate["is_exist"]:
    print "Already exists: " + word.strip()
else:
    context = word_dto.context.encode('utf-8')
    lingualeo.add_word(word, translate["tword"], context)
    print "Add word: " + word.strip()

for word_dto in word_handler.get():
    word = word_dto.text.lower().encode('utf-8')
    translate = lingualeo.get_translates(word)

    if translate["is_exist"]:
        print "Already exists: " + word.strip()
    else:
        context = word_dto.context.encode('utf-8')
        lingualeo.add_word(word, translate["tword"], context)
        print "Add word: " + word.strip()