import subprocess
import sys

scope_name = str(sys.argv[1])

def amass(scope):
	result = subprocess.run(['amass enum --passive -d {}'.format(scope), '-l'], stdout=subprocess.PIPE, shell=True)
	return result.stdout


def get_domains(ins_scope):
	domains1 = []

	wordlist = open('./commonspeak2.txt').read().split('\n')

	for word in wordlist:
		if not word.strip():
			continue
		domains1.append(f"{word.strip()}.{ins_scope}")

	domains2 = amass(ins_scope).decode().split('\n')

	domains = domains1 + domains2

	f = open("autogen_domains.txt", "w")

	for domain in domains:
		f.write(domain)
		f.write('\n')

	f.close()


get_domains(scope_name)

RESOLVERS_PATH = './massdns-master/lists/resolvers.txt'


def massdns():
	result = subprocess.run([f'./massdns-master/bin/massdns -r {RESOLVERS_PATH} -t A -o S -w massdns.out autogen_domains.txt'], stdout=subprocess.PIPE, shell=True)
	success = "Done!"
	return success

print(massdns())

