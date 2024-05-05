from string import Template
import yaml
import itertools

start_template = """
#!/bin/bash
#SBATCH -o $output 
#SBATCH -e $error
#SBATCH -t $time 
#SBATCH -n 1
#SBATCH -N 1
"""

class obj1(object):
    def __iter__(self):
        for i in range(10):
            yield i


def main():
    args = {
        'output' : 'output_file',
        'error' : 'error_file',
        'time' : '24:00:00'
    }
    o1 = obj1()
    o2 = obj1()
    combos = itertools.product(*[o1, o2])
    for c in combos:
        print(c)
    exit()
    params = {"C"     : [.001, .01, .1],
              "gamma" : [.01, 1, 10],
              "kernel": ["linear", "rbf"]}
    keys, values = zip(*params.items())
    for bundle in itertools.product(*values):
        d = dict(zip(keys, bundle))
        print(d)
    exit()
    params = yaml.load(open("params.yml"), Loader=yaml.FullLoader)
    for arg, vals in params.items():
        print(arg, vals)
    exit()
    f = open("default.template")
    lines = f.readlines()
    f.close()
    job_str = "".join(lines)
    t = Template(job_str)
    print(t.substitute(**args))
    pass


if __name__ == "__main__":
    main()
