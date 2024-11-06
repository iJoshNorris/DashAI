# flake8: noqa

# Cross decomposition module
from DashAI.back.converters.scikit_learn.cca import CCA
from DashAI.back.converters.scikit_learn.pls_canonical import PLSCanonical
from DashAI.back.converters.scikit_learn.pls_regression import PLSRegression
from DashAI.back.converters.scikit_learn.pls_svd import PLSSVD

# Decomposition module
from DashAI.back.converters.scikit_learn.dictionary_learning import DictionaryLearning
from DashAI.back.converters.scikit_learn.factor_analysis import FactorAnalysis
from DashAI.back.converters.scikit_learn.fast_ica import FastICA
from DashAI.back.converters.scikit_learn.incremental_pca import IncrementalPCA
from DashAI.back.converters.scikit_learn.kernel_pca import KernelPCA
from DashAI.back.converters.scikit_learn.latent_dirichlet_allocation import (
    LatentDirichletAllocation,
)
from DashAI.back.converters.scikit_learn.mini_batch_dictionary_learning import (
    MiniBatchDictionaryLearning,
)
from DashAI.back.converters.scikit_learn.mini_batch_sparse_pca import MiniBatchSparsePCA
from DashAI.back.converters.scikit_learn.nmf import NMF
from DashAI.back.converters.scikit_learn.mini_batch_nmf import MiniBatchNMF
from DashAI.back.converters.scikit_learn.pca import PCA
from DashAI.back.converters.scikit_learn.sparse_pca import SparsePCA
from DashAI.back.converters.scikit_learn.sparse_coder import SparseCoder
from DashAI.back.converters.scikit_learn.truncated_svd import TruncatedSVD

# Preprocessing module
from DashAI.back.converters.scikit_learn.binarizer import Binarizer
from DashAI.back.converters.scikit_learn.k_bins_discretizer import KBinsDiscretizer
from DashAI.back.converters.scikit_learn.kernel_centerer import KernelCenterer
from DashAI.back.converters.scikit_learn.label_binarizer import LabelBinarizer
from DashAI.back.converters.scikit_learn.label_encoder import LabelEncoder
from DashAI.back.converters.scikit_learn.max_abs_scaler import MaxAbsScaler
from DashAI.back.converters.scikit_learn.min_max_scaler import MinMaxScaler
from DashAI.back.converters.scikit_learn.multi_label_binarizer import (
    MultiLabelBinarizer,
)
from DashAI.back.converters.scikit_learn.normalizer import Normalizer
from DashAI.back.converters.scikit_learn.one_hot_encoder import OneHotEncoder
from DashAI.back.converters.scikit_learn.ordinal_encoder import OrdinalEncoder
from DashAI.back.converters.scikit_learn.polynomial_features import PolynomialFeatures
from DashAI.back.converters.scikit_learn.power_transformer import PowerTransformer
from DashAI.back.converters.scikit_learn.quantile_transformer import QuantileTransformer
from DashAI.back.converters.scikit_learn.robust_scaler import RobustScaler
from DashAI.back.converters.scikit_learn.spline_transformer import SplineTransformer
from DashAI.back.converters.scikit_learn.standard_scaler import StandardScaler

# Discriminant analysis module
from DashAI.back.converters.scikit_learn.linear_discriminant_analysis import (
    LinearDiscriminantAnalysis,
)
from DashAI.back.converters.scikit_learn.quadratic_discriminant_analysis import (
    QuadraticDiscriminantAnalysis,
)

# Feature extraction module
from DashAI.back.converters.scikit_learn.dict_vectorizer import DictVectorizer
from DashAI.back.converters.scikit_learn.feature_hasher import FeatureHasher

# Feature extraction from text module
from DashAI.back.converters.scikit_learn.count_vectorizer import CountVectorizer
from DashAI.back.converters.scikit_learn.hashing_vectorizer import HashingVectorizer
from DashAI.back.converters.scikit_learn.tfidf_transformer import TfidfTransformer
from DashAI.back.converters.scikit_learn.tfidf_vectorizer import TfidfVectorizer

# Feature selection module
from DashAI.back.converters.scikit_learn.generic_univariate_select import (
    GenericUnivariateSelect,
)
from DashAI.back.converters.scikit_learn.select_percentile import SelectPercentile
from DashAI.back.converters.scikit_learn.select_k_best import SelectKBest
from DashAI.back.converters.scikit_learn.select_fpr import SelectFpr
from DashAI.back.converters.scikit_learn.select_fdr import SelectFdr
from DashAI.back.converters.scikit_learn.select_fwe import SelectFwe
from DashAI.back.converters.scikit_learn.variance_threshold import VarianceThreshold
