# Michael Langford
# 3/3/19
# trying to train several models at once

### imports
import os
### end imports

# defining string skeletons to format and execute on command line
input_dir_str = 'INPUT_DIRECTORY=./wtc_performance'
seq_str = 'SEQUENCES_TFRECORD=./notesequences.tfrecord'
config_str = 'CONFIG={}'
generate_str = 'python performance_rnn_generate.py --config={} --run_dir=./logdir/{} --output_dir=./logdir/{}/generated --num_outputs=1 --num_steps=5000 --temperature={} --beam_size={} --branch_factor={} --steps_per_iteration={}'
attn_substr = ' --hparams=\'attn_length\'=128'

# all the configs you want to try

##### WE NEED SOME MORE OF THESE
config_list = ['simple_rnn']#,
				#'performance_with_dynamics_and_modulo_encoding']
config_names = ['simple_rnn']
#####

# generation parameter lists for a grid search
t_list = [0.9]
bs_list = [16]
bf_list = [16]
spi_list = [32]
num_to_gen = 1

# random starting triad!
def make_starting_triad():

	import random

	# first find the root. 
	# 60 is middle c, so let's go within an octave of that
	root = random.randint(48, 72)

	# we'll say it's default minor triad, which would make the second pitch
	# 3 semitones above the root. Add one more to that value if it's major
	major_adjustment = random.randint(0,1)

	triad = '[{},{},{}]'.format(root, root + 3 + major_adjustment, root + 7)

	return triad

# make random ascending scale instead
def make_starting_run():

	import random

	# first find the root
	# 60 is middle c, so we'll start within an octave of that
	# we'll do natural minor scale as a base and then add major adjustment to that
	root = random.randint(48,72)

	# major adjustment
	ma = random.randint(0,1)

	run = '[{},{},{},{},{},{},{}]'.format(
			root,
			root + 2,
			root + 3 + ma,
			root + 5,
			root + 7,
			root + 8 + ma,
			root + 10 + ma)

	return run

# new function to add the primer whatever to the stuff
def add_primer(gen_str):

	import random

	choice = random.randint(0,1)

	# split between run or triad
	if choice == 0:

		# we do a triad
		primer_str = ' --primer_pitches={}'.format(make_starting_triad())

	else:

		# we do a run
		primer_str = ' --primer_melody={}'.format(make_starting_run())

	gen_str += primer_str

	return gen_str


# execute the first definitions
os.system(input_dir_str)
os.system(seq_str)

for i in range(len(config_list)):

	config = config_list[i]
	config_name = config_names[i]

	# grid search!!
	for t in t_list:
		for bs in bs_list:
			for bf in bf_list:
				for spi in spi_list:

					for i in range(num_to_gen):
						
						_generate_str = generate_str.format(config, config_name, config_name, t, bs, bf, spi)

						gen_str = add_primer(_generate_str)

						if 'attn' in config_name:
							gen_str += attn_substr

						os.system(gen_str)

print('Complete!')






