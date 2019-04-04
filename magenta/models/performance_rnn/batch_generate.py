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
#train_str = 'python performance_rnn_train.py --config={} --run_dir=./logdir/{} --sequence_example_file=./sequence_examples/training_performances.tfrecord'
generate_str = 'python performance_rnn_generate.py --config={} --run_dir=./logdir/{} --output_dir=./logdir/{}/generated --num_outputs=1 --num_steps=1000 --primer_pitches=[60,64,67] --temperature={} --beam_size={} --branch_factor={} --steps_per_iteration={}'
attn_substr = ' --hparams=\'attn_length\'=128'

# all the configs you want to try
config_list = ['performance_with_dynamics_and_modulo_encoding']
config_names = ['lstm_attn']

# generation parameter lists for a grid search
t_list = [0.9, 1.0, 1.1]
bs_list = [2, 16, 32]
bf_list = [2, 16, 32]
spi_list = [2, 64, 512]

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

					_generate_str = generate_str.format(config, config_name, config_name, t, bs, bf, spi)

	if 'attn' in config_name:
		_generate_str += attn_substr

	os.system(_generate_str)

print('Complete!')






