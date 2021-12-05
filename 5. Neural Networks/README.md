## Traffic Project

### Objective

Write an AI to identify which traffic sign appears in a photograph.

### Learnings

To build an effective convolutional neural network (CNN) model requires experimentation with adding multiple 2D convolutional and pooling layers. [Ref](https://towardsdatascience.com/the-most-intuitive-and-easiest-guide-for-convolutional-neural-network-3607be47480)

![layers](https://miro.medium.com/max/700/0*usI_HmpFeF2iPBEM.png)

It is also important to flatten the input to ensure multi-dimensional input can be constructed into a single dimension. [Ref](https://stackoverflow.com/questions/43237124/what-is-the-role-of-flatten-in-keras)

To illustrate the the point of adding multiple 2D convolutional and pooling layers here are the results as the experiment progressed all training 10 epochs:

| Convolutional Layers | Accuracy | Loss    |
|----------------------|----------|---------|
| 1                    | 0.0467   | 15.3658 |
| 2                    | 0.0378   | 15.5090 |
| 3                    | 0.9767   | 0.1157  |

The final model included:

- 1 convolutional 2D layer with 32 3x3 filters using [ReLU](https://keras.io/api/layers/activations/#relu-function) activation function
- 1 max pooling layer with 2x2 pool size
- 1 convolutional 2D layer with 64 3x3 filters using [ReLU](https://keras.io/api/layers/activations/#relu-function) activation function
- 1 max pooling layer with 2x2 pool size
- 1 convolutional 2D layer with 64 3x3 filters using [ReLU](https://keras.io/api/layers/activations/#relu-function) activation function
- 1 max pooling layer with 2x2 pool size
- 1 densely-connected layer with units equal to number of categories and using [softmax](https://keras.io/api/layers/activations/#usage-of-activations) activation function

Although this model resulted in an accuracy of 97.67%, a further improvement to the model might include experimenting with adding a [dropout layer](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Dropout) which randomly sets input units to 0 with a frequency of rate at each step during training time, which helps prevent overfitting. 

Update: I went back to test including a dropout layer to the model. 

```python
model.add(
    tf.keras.layers.Dropout(0.2)
)
```

The results are shown in the table below. At the slight lowering of accuracy we can have more confidence the model is better prepared to prevent overfitting.

| Accuracy | Loss    |
|----------|---------|
| 0.9620   | 0.1507  |

