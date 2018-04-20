from ruruki.graphs import Graph
import pandas as pd
import numpy as np
import random
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import euclidean_distances


class gclassifier(BaseEstimator, ClassifierMixin):

 def __init__(self, nbins):
  self.nbins = nbins
  self.graph = Graph()
  print("num of bins="+str(self.nbins))
  print(self.graph)

 def fit(self,X_train, y_train,sample_weight=None):
  nbins = self.nbins
  graph = self.graph
  rows = X_train.shape[0]
  cols = X_train.shape[-1]
  bins = []
  self.classes_ = unique_labels(y_train)
  print(len(self.classes_))

  for kk in range (0,cols):
   bins.append(self.get_buckets(X_train.min(axis=0)[kk],X_train.max(axis=0)[kk],nbins))

  self.bins = bins

  for i in range (0,rows):
    for j in range (0,cols):
        wbin=self.find_bin(bins[j],X_train[i][j])
        #print("wbin"+str(wbin))
        v = graph.get_or_create_vertex("data",col=j,cbin=wbin)
        out = graph.get_or_create_vertex("outc",out=y_train[i])
        #print(out)
        edge = graph.get_or_create_edge(v, "outcome", out)
        if(edge.as_dict().get('properties').get("count") == None):
            edge.set_property(count=1)
        else:
            cc = int(str(edge.as_dict().get('properties').get("count")))+1
            edge.set_property(count=cc)
  return

 def predict(self,X_test):
  graph = self.graph
  y_pred =[]
  for i in range (0,X_test.shape[0]):
      count= np.zeros(len(self.classes_))
      totv = []
      for j in range (0,X_test.shape[-1]):
          wbin=self.find_bin(self.bins[j],X_test[i][j])
          for v in graph.get_vertices("data",col=j,cbin=wbin):
              totv.append(v)
      for r in totv:
          mv = r
          #print(mv.as_dict().get('properties'))
          for m in mv.get_out_edges():
                  #print(m.as_dict().get('properties'))
                  #print(m.get_out_vertex().as_dict())
                  indx = int(str(m.get_out_vertex().as_dict().get('properties').get("out")))
                  count[indx] = count[indx]+int(str(m.as_dict().get('properties').get("count")))
                  #print("index"+str(indx)+" --"+str(count[indx]))
      #print(count)
      for ii in range (0,len(count)):
          if(count[ii] == count.max()):
                  #print(self.classes_[ii])
                  y_pred.append(self.classes_[ii])
                  break
  return y_pred

 def get_buckets(self,min, max, num_buckets):
   buckets = []
   bucket_size= (max-min)/num_buckets
   for i in range(1,num_buckets):
    buckets.append((min+(i-1)*bucket_size))
   buckets.append(max)
   return buckets

 def find_bin(self,abins,value):
  first_bin = abins[0]
  for i in range (1,len(abins)):
   if (value >= first_bin and value <= abins[i]):
    return i
   else:
    first_bin = abins[i]
  return -1

def get_params(self, deep=True):
    # suppose this estimator has parameters "alpha" and "recursive"
    return {"nbins": self.nbins}

def set_params(self, **parameters):
    for parameter, value in parameters.items():
        setattr(self, parameter, value)
    return self
