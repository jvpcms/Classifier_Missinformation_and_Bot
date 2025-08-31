from classifier.bluesky_user_classifier import (
    BlueSkyUserClassifier,
    DecisionTreeBlueSkyUserClassifier,
    KNNBlueSkyUserClassifier,
    LogisticRegressionBlueSkyUserClassifier,
    NeuralNetworkBlueSkyUserClassifier,
    RandomForestBlueSkyUserClassifier,
)


class ClassifiersCollection:

    knn_user_bot_classifier: BlueSkyUserClassifier
    decision_tree_user_bot_classifier: BlueSkyUserClassifier
    random_forest_user_bot_classifier: BlueSkyUserClassifier
    logistic_regression_user_bot_classifier: BlueSkyUserClassifier
    neural_network_user_bot_classifier: BlueSkyUserClassifier

    def __init__(self):
        self.knn_user_bot_classifier = KNNBlueSkyUserClassifier()
        self.decision_tree_user_bot_classifier = DecisionTreeBlueSkyUserClassifier()
        self.random_forest_user_bot_classifier = RandomForestBlueSkyUserClassifier()
        self.logistic_regression_user_bot_classifier = (
            LogisticRegressionBlueSkyUserClassifier()
        )
        self.neural_network_user_bot_classifier = NeuralNetworkBlueSkyUserClassifier()


def get_classifiers_collection() -> ClassifiersCollection:
    return ClassifiersCollection()
