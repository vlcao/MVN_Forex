def merge(in_files, out_file):
    
    data_set = dict()
    
    for file_name in in_files:
        f = open(file_name, 'r')
        for line in f:
            line = line.strip()
            if line == '': continue
            p1, p2, p3 = line.split(',', 2)
            data_set[p1 + ',' + p2] = p3
    
    File = open(out_file, 'w')
    for key in sorted(data_set):
        File.write('%s,%s\n' % (
            str(key), str(data_set[key])))
    
    return

def main():
    original_files = [
        'AUDCAD1.csv',
        'AUDJPY1.csv',
        'AUDUSD1.csv',
        'CADJPY1.csv',
        'EURCAD1.csv',
        'EURGBP1.csv',
        'EURJPY1.csv',
        'EURUSD1.csv',
        'GBPJPY1.csv',
        'GBPUSD1.csv',
        'USDCAD1.csv',
        'USDJPY1.csv'
    ]
    for file in original_files:
        merge(['o/' + file, 'm/' + file], file)
    return

if __name__ == "__main__":
    main()