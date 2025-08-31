import pandas as pd
from pandas.core.frame import Axes
from models.bluesky_user_model import BlueSkyUser

import pickle

from typing import Union, cast

from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier


class BlueSkyUserClassifier:

    pickle_file_path: str
    classifier: Union[
        KNeighborsClassifier,
        DecisionTreeClassifier,
        RandomForestClassifier,
        LogisticRegression,
        MLPClassifier,
        None,
    ] = None

    def __init__(self, pickle_file_path: str):
        self.pickle_file_path = pickle_file_path
        self.unpickle_classifier()

    def unpickle_classifier(self):
        with open(self.pickle_file_path, "rb") as file:
            self.classifier = pickle.load(file)

    def is_bot(self, user: BlueSkyUser) -> bool:
        """
        Classify a user as bot or not bot.
        """

        if self.classifier is None:
            raise ValueError("Classifier not loaded.")

        # Define the same feature names used during training
        feature_names = [
            "CreatedAt",
            "NumberOfFollowings",
            "NumberOfFollowers",
            "NumberOfTweets",
            "LengthOfScreenName",
            "LenDescrInUseProfile",
        ]

        features = [
            [
                user.datetime.timestamp() if user.datetime is not None else 0,
                user.follows_count,
                user.followers_count,
                user.posts_count,
                len(user.handle) if user.handle is not None else 0,
                len(user.about) if user.about is not None else 0,
            ]
        ]

        # Wrap features in a DataFrame with column names
        features_df = pd.DataFrame(features, columns=cast(Axes, feature_names))

        prediction = self.classifier.predict(features_df)

        if prediction is None or len(prediction) == 0:
            return False

        return prediction[0] == 1


class KNNBlueSkyUserClassifier(BlueSkyUserClassifier):

    def __init__(self):
        super().__init__("./classifier/pickles/k_nearest_neighbors.pkl")
        self.unpickle_classifier()


class DecisionTreeBlueSkyUserClassifier(BlueSkyUserClassifier):

    def __init__(self):
        super().__init__("./classifier/pickles/decision_tree.pkl")
        self.unpickle_classifier()


class RandomForestBlueSkyUserClassifier(BlueSkyUserClassifier):

    def __init__(self):
        super().__init__("./classifier/pickles/random_forest.pkl")
        self.unpickle_classifier()


class LogisticRegressionBlueSkyUserClassifier(BlueSkyUserClassifier):

    def __init__(self):
        super().__init__("./classifier/pickles/logistic_regression.pkl")
        self.unpickle_classifier()


class NeuralNetworkBlueSkyUserClassifier(BlueSkyUserClassifier):

    def __init__(self):
        super().__init__("./classifier/pickles/neural_network.pkl")
        self.unpickle_classifier()


# Debugging utility to inspect the classifier
def inspect_classifier(model):

    print("=== Model Type ===")
    print(type(model))
    print("==================\n")

    # If it's a pipeline, list steps
    if isinstance(model, Pipeline):
        print("Pipeline detected. Steps:")
        for name, step in model.named_steps.items():
            print(f"  - {name}: {step.__class__.__name__}")
        print()

        final_estimator = model.steps[-1][1]  # last step
    else:
        final_estimator = model

    print("=== Classifier Details ===")
    if hasattr(final_estimator, "n_features_in_"):
        print("Number of features expected:", final_estimator.n_features_in_)

    # Try feature names at different levels
    feature_names = None
    if hasattr(final_estimator, "feature_names_in_"):
        feature_names = list(final_estimator.feature_names_in_)
    else:
        # check pipeline steps
        if isinstance(model, Pipeline):
            for name, step in model.named_steps.items():
                if hasattr(step, "feature_names_in_"):
                    feature_names = list(step.feature_names_in_)
                    break

    if feature_names:
        print("Feature names:", feature_names)
    else:
        print("⚠️ No feature names stored in the pickle (only number of features).")

    if hasattr(final_estimator, "classes_"):
        print("Classes:", final_estimator.classes_)

    if hasattr(final_estimator, "n_classes_"):
        print("Number of classes:", final_estimator.n_classes_)

    print("==========================")
