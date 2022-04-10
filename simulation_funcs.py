import numpy as np
import pandas as pd
import math


#def poisson_probability(actual, mean):
#    # naive:   math.exp(-mean) * mean**actual / factorial(actual)
#    # iterative, to keep the components from getting too large or small:
#    p = math.exp(-mean)
#    for i in range(actual):
#        p *= mean
#        p /= i+1
#    return p

def bowling_simulation(data, itterations):
    data.columns = ['Runner', 'Mean']
    samples = pd.DataFrame(data=range(itterations), columns=['sample_no'])
    for runner in range(len(data)):
        samples[data['Runner'][runner]] = np.random.poisson(data['Mean'][runner], itterations)
    scores = samples.drop(columns=['sample_no'])
    scores['no_winners'] = [sum(i) for i in scores.values == scores.max(axis=1)[:, None]]
    scores['max'] = scores.max(axis=1)
    scores = np.floor((scores.drop(columns=['max', 'no_winners'])+1).div(scores['max']+1, axis=0)).div(scores['no_winners'], axis=0)
    odds = itterations/scores.sum()
    return odds

#df = pd.DataFrame ({'Player': ['ST Gabriel', 'JO Holder', 'KAJ Roach', 'RL Chase', 'AS Joseph'], 'Mean': [2.4,2.0,2.6,1.1,1.7]}, columns = ['Player','Mean'])
#simulation(df, 10000)

def batting_simulation(data, itterations):
    data.columns = ['Runner', 'Mean']
    samples = pd.DataFrame(data=range(itterations), columns=['sample_no'])
    for runner in range(len(data)):
        samples[data['Runner'][runner]] = np.random.exponential(data['Mean'][runner], itterations)
    scores = samples.drop(columns=['sample_no'])
    scores['no_winners'] = [sum(i) for i in scores.values == scores.max(axis=1)[:, None]]
    scores['max'] = scores.max(axis=1)
    scores = np.floor(scores.drop(columns=['max', 'no_winners']).div(scores['max'], axis=0)).div(scores['no_winners'], axis=0)
    odds = itterations / scores.sum()
    return odds

def sixes_simulation(data, itterations):
    data.columns = ['Runner', 'Mean']
    samples = pd.DataFrame(data=range(itterations), columns=['sample_no'])
    for runner in range(len(data)):
        samples[data['Runner'][runner]] = np.random.negative_binomial(data['Mean'][runner], 0.5, itterations)
    scores = samples.drop(columns=['sample_no'])
    scores['Winner'] = [data['Runner'][0] if i>j else data['Runner'][1] if i<j else 'Tie' for i,j in zip(samples[data['Runner'][0]],samples[data['Runner'][1]])]
    odds = scores[['Winner', data['Runner'][0]]].groupby('Winner').agg('count').reset_index()
    odds.columns = ['Team', 'Odds']
    odds['Odds'] = itterations / odds['Odds']
    return odds

