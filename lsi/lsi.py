import os;
import sys;
import svd;
from scipy import linalg;
import numpy;

class WordSegment:
  def __init__(self):
    pass;

  def segment_word(self, line):
    return [];

class SimpleWordSegment(WordSegment):

  def __init__(self):
    pass;

  def segment_word(self, line):
    result = [];
    splits_by_space = line.split(' ');
    for words in splits_by_space:
      result.append(words);
    return result;


# The document-to-word vector representaton of text corpus
#
class DocumentWordVector:
  
  def __init__(self, word_segment=None):
    self._dict_ = set();
    self._doc_ = [];
    self._vsm_ = [];
    self._word_segment = word_segment;
    if word_segment == None:
      self._word_segment = SimpleWordSegment();

  #set the document source directory and parse
  # to word
  def set_source(self, directory):
    files = os.listdir(directory);
    #first pass, build dictionary
    for file in files:
      fullfile = os.path.join(directory, file);
      if os.path.isfile(fullfile):
        fd = open(fullfile, 'r');
        self._doc_.append(file);
        for line in fd:
          words = self._word_segment.segment_word(line);
          for word in words:
            self._dict_.add(word);
        #finish the reading, closing
        fd.close();
    print self._dict_;
    #second pass, build vector-space-model matrix
    for file in files:
      vector = [];
      worddict = {};
      fullfile = os.path.join(directory, file);
      if os.path.isfile(fullfile):
        fd = open(fullfile, 'r');
        for line in fd:
          words = self._word_segment.segment_word(line);
          for word in words:
            if worddict.has_key(word):
              worddict[word] = worddict[word] + 1;
            else:
              worddict[word] = 1;
        for word in self._dict_:
          if word in worddict:
            vector.append(worddict[word]);
          else:
            vector.append(0);
        #add the vector model to the matrix
        self._vsm_.append(vector);
    #reverse the vsm to term-document matrix
    vsm = [];
    for i in range(len(self._vsm_[0])):
      vector = [];
      for j in range(len(self._vsm_)):
        vector.append(self._vsm_[j][i]);
      print vector;
      vsm.append(vector);
    self._vsm_ = vsm;
    print self._vsm_;

  def get_vsm(self):
    return self._vsm_;
  

class LatentSemanticIndex:
  
  def __init__(self):
    self._U_ = [];  # the U matrix
    self._SIGMA_ = [];  # the engine vector
    self._Vh_ = [];  # the V matrix
    self.M = 0;
    self.N = 0;
  
  def svd(self, matrix):
    matrix = numpy.mat(matrix);
    self._U_, self._SIGMA_, self._Vh_ = linalg.svd(matrix);
    #do the svd 
    self.M, self.N = matrix.shape;
    Sig = numpy.mat(linalg.diagsvd(self._SIGMA_, self.M, self.N)) 
    print Sig
    #print (U_) * (Sig) * (Vh_);

  def dimension_reduction(self, target_dim):
    UList = [];
    SIGMA = [];
    VList = [];
    for i in range(target_dim):
      UList.append(self._U_[i,:].tolist());
      SIGMA.append(self._SIGMA_[i]);
      VList.append(self._Vh_[:,i].tolist());
     
    ReducedU = numpy.mat(UList);
    print ReducedU.transpose();
    ReducedU = ReducedU.transpose();
    ReducedVh = numpy.mat(VList);
    print ReducedVh;
    Sig = numpy.mat(linalg.diagsvd(SIGMA,target_dim,target_dim)) 
    print Sig
    
    #construct the new matrix
    newMatrix =  (ReducedU) * (Sig) * (ReducedVh);
    pass; 

vsm = DocumentWordVector();
vsm.set_source('/Users/liushouqun/Development/github/text-mining/lsi/test') 

lsi = LatentSemanticIndex();
lsi.svd(vsm.get_vsm());
lsi.dimension_reduction(1);

