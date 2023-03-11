import json


class SwaggerMerger(object):
    
    ## Constructor
    def __init__(self, input1=None, input2=None, output=None):
        self.input1 = input1
        self.input2 = input2
        self.output = output

    ## Recursive function to merge two dictionaries and output a new dictionary.
    def recursive_merge(self, d1, d2):
        d = {}
        for key, value in d1.items():
            if key in d2:
                if ((type(d1[key]) is dict) and type(d2[key]) is dict):
                    d[key] = self.recursive_merge(d1[key], d2[key])
                if (type(value) is not dict):
                    if (d1[key] == d2[key]):
                        d[key] = value # copy non-dict value eg string
                    else:
                        d[key] = [d1[key], d2[key]] #append conflicts into a list
            else:
                d[key] = value # shallow copy the value
        for key, value in d2.items():
            if key not in d1:
                d[key] = value
        return d


    ## Test it on actual json files
    def run(self):
        infile1 = open(self.input1, 'r')
        infile2 = open(self.input2, 'r')

        data1 = json.load(infile1)
        data2 = json.load(infile2)

        data3 = self.recursive_merge(data1, data2)

        output_file = open(self.output, 'w')
        json.dump(data3, output_file, indent=4)


if __name__ == '__main__':
    input_files=['../account-service/docs/swagger.json','../payment-service/docs/swagger.json']
    output_file = '../gateway-service/docs/swagger.json'

    sm = SwaggerMerger(input1=input_files[0], input2=input_files[1], output=output_file)
    sm.run()


