# Michael Langford
# 3/3/19
# trying to train several models at once

### imports
import os
### end imports

# mode!
mode = 'train and generate' # 'train', 'generate', or 'train and generate'

# defining string skeletons to format and execute on command line
input_dir_str = 'INPUT_DIRECTORY=./wtc_performance'
seq_str = 'SEQUENCES_TFRECORD=./notesequences.tfrecord'
config_str = 'CONFIG={}'
train_str = 'python performance_rnn_train.py --config={} --run_dir=./logdir/{} --sequence_example_file=./sequence_examples/training_performances.tfrecord'
generate_str = 'python performance_rnn_generate.py --config={} --run_dir=./logdir/{} --output_dir=./logdir/{}/generated --num_outputs=1 --num_steps=1000 --primer_pitches={} --temperature=1.0 --beam_size=10 --branch_factor=20 --steps_per_iteration=10'
attn_substr = ' --hparams=\'attn_length\'=100'

# all the configs you want to try
config_list = [#'performance_with_dynamics_and_modulo_encoding', 
				'performance_with_dynamics_and_modulo_encoding', 
				'gru', 
				'indy_gru', 
				'glstm', 
				'intersection_rnn', #####
				'ugrnn']
config_names = [#'lstm', 
				'lstm_attn', 
				'gru_attn', 
				'indy_gru_attn', 
				'glstm_attn', 
				'intersection_attn', #####
				'ugrnn_attn']


# function to choose the starting triad
def make_starting_triad():

	import random

	# first find the root. 
	# 60 is middle c, so let's go within an octave of that
	root = random.randint(48, 73)

	# we'll say it's default minor triad, which would make the second pitch
	# 3 semitones above the root. Add one more to that value if it's major
	major_adjustment = random.randint(0,2) # 2 shouldn't be included in this

	triad = '[{},{},{}]'.format(root, root + 3 + major_adjustment, root + 7)

	return triad

# execute the first definitions
os.system(input_dir_str)
os.system(seq_str)

for i in range(len(config_list)):

	config = config_list[i]
	config_name = config_names[i]

	if mode == 'train' or mode == 'train and generate':
		
		_train_str = train_str.format(config, config_name)

		if 'attn' in config_name:
			_train_str += attn_substr

		os.system(_train_str)

	if mode == 'generate' or mode == 'train and generate':

		triad = make_starting_triad()

		_generate_str = generate_str.format(config, config_name, config_name, triad)

		if 'attn' in config_name:
			_generate_str += attn_substr

		os.system(_generate_str)

print('Complete!')






