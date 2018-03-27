#
#
#
#Tensorflow model for watermelon ripeness
#

import tensorflow as tf

def model(features,labels,mode):
	input_layer = tf.reshape(features["x"],[-1,28,28,1]);


	conv = tf.layers.conv2d(
		input_layer,
		filters=32,
		kernel_size=[4,4],
		padding="same",
		activation=tf.nn.relu)
	pool = tf.layers.max_pooling2d(
		inputs=conv,
		pool_size=[2,2],
		strides = 2)

	#Dense layer
	pool_flat = tf.reshape(pool,[-1,14*14*32])

	dense = tf.layers.dense(
		inputs=pool_flat,
		units=1024,
		activation=tf.nn.relu)
	dropout = tf.layers.dropout(
		inputs =dense ,
		rate=.4,
		training=mode == tf.estimator.ModeKeys.TRAIN)
	logits = tf.layers.dense(inputs=dropout,units=2)

	predictions = {
		"classes": tf.argmax(input=logits,axis=1),
		"probabilites":tf.nn.softmax(logits,name="softmax_tensor")
	}
	if mode == tf.estimator.ModeKeys.PREDICT:
		outputs ={
			"predictions": tf.estimator.export.PredictOutput(predictions),
		}
		return tf.estimator.EstimatorSpec(mode=mode,predictions=predictions,
			export_outputs=outputs)

	loss = tf.losses.sparse_softmax_cross_entropy(labels=labels,logits=logits)

	if mode == tf.estimator.ModeKeys.TRAIN:
		optimizer = tf.train.GradientDescentOptimizer(learning_rate=.001)
		train_op = optimizer.minimize(
			loss = loss,
			global_step=tf.train.get_global_step())
		return tf.estimator.EstimatorSpec(mode=mode,loss=loss,train_op=train_op)

	eval_metric_ops = {
		"accuracy" : tf.metrics.accuracy( 
			labels=labels,predictions=predictions["classes"])
	}
	return tf.estimator.EstimatorSpec(mode=mode,loss=loss,eval_metric_ops=eval_metric_ops);

