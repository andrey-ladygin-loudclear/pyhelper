import shlex


class ParseCommandArguments:
    def __init__(self, string):
        self.string = string

    def parse(self):
        args = []
        components = shlex.split(self.string)
        added = ''

        for i in range(len(components)):
            key = components[i]

            if key == added:
                continue

            if ':' in key:
                args.append({key.split(':')[0]: key.split(':')[1]})
                continue

            try:
                val = components[i+1]
            except IndexError:
                val = ''

            if '-' in key and '-' not in val:
                args.append({key: val})
                added = val
            else:
                args.append({key: ''})

        return args

        #create:controller -p /var/www/tvpli -n:"FeedbackReports as" -uploads image,icon,profile -namespace Admin -dest "/home/andrey/Desktop test"