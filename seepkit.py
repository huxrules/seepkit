# Seepkit has been developed by Huxlabs LLC to be a quick command line
# python program that will take *.wcd or *.all files and using a custom
# CNN will search for seeps.
# The CNN was trained on NOAA EX1105 multibeam data. 
# The script will parse watercolumn data, if it exists, from Kongsberg
# EM302 and EM2040 multibeams
# 
# the switches that can be used are
# -l "path to file" use a list of files 
# the list of files should be a text file that has the entire path to the 
# multibeam files in question
# as an example in bash you can use the following command
# ls -d -1 $PWD/*.* > "filename.txt"
# to make a list of files, complete with path
# -s "path to single file" - should be self explanitory
# -o "filename" - record the output to a file, without this switch the output
# will be written to standard output


import argparse

#import sonar_data_control as SDC

def runProgramWithListOfFiles(filelist,output):
	

def runProgramWithSingleFile(filename,output):
	pass

if __name__ == "__main__":
	descriptionText = """
SeepKit v 0.1 by Huxlabs LLC
"""
	commandParser = argparse.ArgumentParser(description = descriptionText)
	commandParser.add_argument("-l","--list",help="path to a textfile containing a list of files")
	commandParser.add_argument("-f","--file",help="path to a single file")
	commandParser.add_argument("-o","--output",help="path to the ouput file, if not given will output to stdout")
	args = commandParser.parse_args()
	#print(args.list)
	if args.output:
		outputfile = args.output
	else:
		outputfile = None

	if args.list and args.file:
		print('Cannot use both a list and a single file, check your switches')
	elif args.list and not args.file:
		print("list mode")
		status = runProgramWithListOfFiles(args.list, outputfile)
	elif args.file and not args.list:
		print("single file mode")
		status = runProgramWithSingleFile(args.file, outputfile)


"""
	if len(commandLineSwitches) == 1:
		print("No CL switches, use -h for help")
	else:
		if len(commandLineSwitches) > 5:
			print("Too many switches, use -h for help")
		else:
			LOFbreak = 0
			SFbreak = 0
			OUTbreak = 0
			HELPbreak = 0
			
			for a in commandLineSwitches[1:len(commandLineSwitches)]:

				if a == "-l":
					if LOFbreak == 0:
						listOfFiles = commandLineSwitches[commandLineSwitches.index("-l") + 1]
						LOFbreak = 1
					elif LOFbreak == 1:
						print("only one -l switch, use -h for help")
				if a == "-s":
					if SFbreak == 0:
						singleFile = commandLineSwitches[commandLineSwitches.index("-s") + 1]
						SFbreak = 1
					elif SFbreak == 1:				
						print("only one -s switch, use -h for help")
"""