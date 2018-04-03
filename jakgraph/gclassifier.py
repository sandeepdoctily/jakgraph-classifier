from ruruki.graphs import Graph
import pandas as pd
import numpy as np
import random

class gclassifier:

 def __init__(self, bins):
  self.nbins = bins
  self.graph = Graph()
  print("num of bins="+str(self.nbins))
  print(self.graph)

 def fit(self,X_train, y_train):
  print("Hello")
  nbins = self.nbins
  graph = self.graph
  rows = X_train.shape[0]
  cols = X_train.shape[-1]
  bins = []
  self.response_classes = np.array(list(set(y_train)))
  print(len(self.response_classes))

  for kk in range (0,cols):
   bins.append(self.get_buckets(X_train.min(axis=0)[kk],X_train.max(axis=0)[kk],nbins))

  self.bins = bins

  for i in range (0,rows):
    for j in range (0,cols):
        wbin=self.find_bin(bins[j],X_train[i][j])
        print("wbin"+str(wbin))
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
      count= np.zeros(len(self.response_classes))
      totv = []
      for j in range (0,X_test.shape[-1]):
          wbin=self.find_bin(self.bins[j],X_test[i][j])
          for v in graph.get_vertices("data",col=j,cbin=wbin):
              totv.append(v)
      for r in totv:
          mv = r
          print(mv.as_dict().get('properties'))
          for m in mv.get_out_edges():
                  #print(m.as_dict().get('properties'))
                  #print(m.get_out_vertex().as_dict())
                  indx = int(str(m.get_out_vertex().as_dict().get('properties').get("out")))
                  count[indx] = count[indx]+int(str(m.as_dict().get('properties').get("count")))
                  #print("index"+str(indx)+" --"+str(count[indx]))
      print(count)
      for ii in range (0,len(count)):
          if(count[ii] == count.max()):
                  print(self.response_classes[ii])
                  y_pred.append(self.response_classes[ii])
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
