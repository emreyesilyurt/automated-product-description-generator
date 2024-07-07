import openai
import numpy as np

class LLM_Agent:
    def __init__(self, actions):
        self.q_table = {}
        self.actions = actions
        self.learning_rate = 0.1
        self.discount_factor = 0.99
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995

    def get_state(self, environment):
        return str(environment)

    def choose_action(self, state):
        if np.random.rand() < self.exploration_rate:
            return np.random.choice(self.actions)
        return self.get_best_action(state)

    def get_best_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))
        return self.actions[np.argmax(self.q_table[state])]

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.actions))
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(len(self.actions))
        
        action_index = self.actions.index(action)
        best_next_action = np.max(self.q_table[next_state])
        td_target = reward + self.discount_factor * best_next_action
        td_error = td_target - self.q_table[state][action_index]
        self.q_table[state][action_index] += self.learning_rate * td_error

    def query_llm(self, prompt):
        response = openai.Completion.create(
            engine="gpt-4-turbo",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def train(self, environment, episodes):
        for _ in range(episodes):
            state = self.get_state(environment.reset())
            done = False

            while not done:
                action = self.choose_action(state)
                next_state, reward, done = environment.step(action)
                next_state = self.get_state(next_state)

                self.update_q_table(state, action, reward, next_state)
                state = next_state

            self.exploration_rate *= self.exploration_decay
