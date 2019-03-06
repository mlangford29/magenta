# Michael Langford
# 3/3/19
# trying to train several models at once

### imports
import os
### end imports

# mode!
mode = 'train' # 'train', 'generate', or 'train and generate'

# defining string skeletons to format and execute on command line
input_dir_str = 'INPUT_DIRECTORY=./wtc_performance'
seq_str = 'SEQUENCES_TFRECORD=./notesequences.tfrecord'
config_str = 'CONFIG={}'
train_str = 'performance_rnn_train --config={} --run_dir=./logdir/{}_test --sequence_example_file=./sequence_examples/training_performances.tfrecord'
generate_str = 'performance_rnn_generate --config=${} --run_dir=./logdir/{}_test --output_dir=run_dir/generated --num_outputs=1 --num_steps=500 primer_pitches=[60,64,67,70] temperature=0.9 beam_size=10 branch_factor=20 steps_per_iteration=10'
attn_substr = ' --hparams=\'attn_length\'=100'

# all the configs you want to try
config_list = ['performance_with_dynamics', 'gru', 'indy_gru', 'grid_lstm', 'bidirectional_grid_lstm',
				'phased_lstm', 'glstm', 'timefreq_lstm', 'intersection_rnn', 'simple_rnn']
config_names = ['pwd_attn', 'gru_attn', 'indy_gru_attn', 'grid_lstm_attn',
				'bi_grid_lstm_attn', 'glstm_attn', 'timefreq_lstm_attn', 'intersection_attn',
				'simple_rnn']

config_to_name = zip(config_list, config_names)

# execute the first definitions
os.system(input_dir_str)
os.system(seq_str)

for config in config_list:

	config_name = config_to_name[config]

	if mode == 'train' or mode == 'train and generate':
		
		_train_str = train_str.format(config, config_name)

		if 'attn' in config_name:
			_train_str += attn_substr

	os.system(_train_str)


	if mode == 'generate' or mode == 'train and generate':

		_generate_str = generate_str.format(config, config_name)

		if 'attn' in config_name:
			_generate_str += attn_substr

		os.system(_generate_str)

print('Complete!')






