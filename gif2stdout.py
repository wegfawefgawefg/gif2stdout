import argparse
from PIL import Image
from sys import stdout

def gif2txt(filename, maxLen=80, output_file='out.html', with_color=False):
    try:
        maxLen = int(maxLen)
    except:
        maxLen = 80

    chs = "MNHQ$OC?7>!:-;. "

    try:
        image = Image.open(filename)
    except IOError:
        exit("file not found: {}".format(filename))

    width, height = image.size
    rate = float(maxLen) / max(width, height)
    width = int(rate * width)
    height = int(rate * height)

    palette = image.getpalette()
    strings = []

    try:
        while True:
            image.putpalette(palette)
            im = Image.new('RGB', image.size)
            im.paste(image)
            im = im.resize((width, height))
            string = ''
            for h in range(height):
                for w in range(width):
                    rgb = im.getpixel((w, h))
                    string += chs[int(sum(rgb) / 3.0 / 256.0 * 16)]
                string += '\n'
            if isinstance(string, bytes):
                string = string.decode('utf8')
            strings.append(string)
            image.seek(image.tell() + 1)
    except EOFError:
        pass

    for string in strings:
        stdout.write( string )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help='Gif input file')
    parser.add_argument('-m', '--maxLen', type=int,
                        help='Max width of the output gif')
    parser.add_argument('-o', '--output',
                        help='Name of the output file')
    parser.add_argument('-c', '--color', action='store_true',
                        default=False,
                        help='With color')
    args = parser.parse_args()

    if not args.maxLen:
        args.maxLen = 80
    if not args.output:
        args.output = 'out.html'

    gif2txt(filename=args.filename,
            maxLen=args.maxLen,
            output_file=args.output,
            with_color=args.color)

if __name__ == '__main__':
    main()
