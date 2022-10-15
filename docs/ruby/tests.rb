
def test_invalid_entry
  a,b,c,d = blah('XXYYY'), blah('XYYXX'), blah('XYYXY'), blah('?YYXX')
  scores = company_score(sentence=false, profound=false, a,b,c,d)
  assert_equal([[4,8,5,3,3],[4,3,5,4,4],[4,3,5,4,3],[-2,3,5,4,4]], scores)
  assert_sums([23, 20, 19, 14], scores)
  assert_equal(total=76, sum(scores))
  total
end

def test_all_Xs_and_Ys
  a,b,c,d = blah('XXYYY'), blah('XYYXX'), blah('XYYXY'), blah('XYYXX')
  scores = company_score(sentence=false, profound=false, a,b,c,d)
  assert_equal([[4,8,5,3,3],[4,3,5,4,4],[4,3,5,4,3],[4,3,5,4,4]], scores)
  assert_sums([23, 20, 19, 20], scores)
  assert_equal(total=82, sum(scores))
  total
end

def test_letters_from_heading
  a,b,c,d = blah('BigFi'), blah('shLit'), blah('tlePo'), blah('ndWaR')
  scores = company_score(sentence=false, profound=false, a,b,c,d)
  assert_equal([[1,-1,1,2,-1],[4,8,16,-1,32],[0,0,-1,0,-1],[0,256,512,-1,1024]], scores)
  assert_sums([2, 59, -2, 1791], scores)
  assert_equal(total=1850, sum(scores))
  total
end

def test_only_lowercase_letters_from_heading
  a,b,c,d = blah('bigfi'), blah('shlit'), blah('tlepo'), blah('ndwar')
  scores = company_score(sentence=false, profound=false, a,b,c,d)
  assert_equal([[10,-10,10,20,-10],[40,80,160,-10,320],[0,0,-10,0,-10],[0,2560,5120,-10,10240]], scores)
  assert_sums([20, 590, -20, 17910], scores)
  assert_equal(total=18500, sum(scores))
  total
end

def test_only_lowercase_consonants_from_heading
  a,b,c,d = blah('bgfsh'), blah('lttlp'), blah('ndwrb'), blah('gfshl')
  scores = company_score(sentence=false, profound=false, a,b,c,d)
  assert_equal([[10,10,20,40,80],[160,320,0,0,0],[0,2560,5120,10240,10],[10,20,0,0,160]], scores)
  assert_sums([160, 480, 17930, 190], scores)
  assert_equal(total=18760, sum(scores))
  total
end

def test_only_lowercase_consonants_near_end_of_heading
  a,b,c,d = blah('rrrrr'), blah('rrrrr'), blah('rrrrr'), blah('rrrrr')
  scores = company_score(sentence=false, profound=false, a,b,c,d)
  assert_equal([[0,10240,0,0,0],[0,0,10240,0,0],[0,0,0,10240,0],[0,0,0,0,10240]], scores)
  assert_sums([10240, 10240, 10240, 10240], scores)
  assert_equal(total=40960, sum(scores))
  total
end

def test_unconnected_lowercase_5_letter_words
  a,b,c,d = word('dwarf'), word('rules'), word('knife'), blah('wwwww')
  scores = company_score(sentence=false, profound=false, a,b,c,d)
  assert_equal([[0,0,-100,0,200],[0,-100,1600,-100,400],[0,0,-100,200,-100],[0,0,0,5120,0]], scores)
  assert_sums([100, 1800, 0, 5120], scores)
  assert_equal(total=7020, sum(scores))
  total
end

def test_sentence_of_lowercase_5_letter_words
  a,b,c,d = word('wrong'), word('words'), word('score'), word('small')
  scores = company_score(sentence=true, profound=false, a,b,c,d)
  assert_equal([[5120000,10240000,-10000,1280000,10000],[0,-10000,0,0,40000],[0,0,-10000,0,-10000],[40000,0,-10000,160000,0]], scores)
  assert_sums([16640000, 30000, -20000, 190000], scores)
  assert_equal(total=16840000, sum(scores))
  total
end

def test_better_sentence_of_lowercase_5_letter_words
  a,b,c,d = word('wrote'), word('wrong'), word('wrote'), word('wrath')
  scores = company_score(sentence=true, profound=false, a,b,c,d)
  assert_equal([[5120000,10240000,-10000,320000,-10000],[0,0,-10000,1280000,10000],[0,0,-10000,0,-10000],[0,0,-10000,320000,80000]], scores)
  assert_sums([15660000, 1280000, -20000, 390000], scores)
  assert_equal(total=17310000, sum(scores))
  total
end

def test_profound_sentence_of_lowercase_5_letter_words
  a,b,c,d = word('waits'), word('while'), word('world'), word('warms')
  scores = company_score(sentence=true, profound=true, a,b,c,d)
  assert_equal([[51200000,-100000,-100000,0,0],[0,800000,-100000,1600000,-100000],[51200000,-100000,102400000,0,0],[0,-100000,0,0,400000]], scores)
  assert_sums([51000000, 2200000, 153500000, 300000], scores)
  assert_equal(total=207000000, sum(scores))
  total
end

def test_example_with_only_3_squads
  a,b,c = word('waits'), word('while'), word('world')
  scores = company_score(sentence=true, profound=true, a,b,c)
  assert_equal([[51200000,-100000,-100000,0,0],[0,800000,-100000,1600000,-100000],[51200000,-100000,102400000,0,0]], scores)
  assert_sums([51000000, 2200000, 153500000], scores)
  assert_equal(total=206700000, sum(scores))
  total
end

def sorted?(array)
  array.each_cons(2).all? { |a, b| (a <=> b) < 0 }
end

def test_scores_increase_as_cookies_are_unlocked
  s0 = test_invalid_entry
  s1 = test_all_Xs_and_Ys
  s2 = test_letters_from_heading
  s3 = test_only_lowercase_letters_from_heading
  s4 = test_only_lowercase_consonants_from_heading
  s5 = test_only_lowercase_consonants_near_end_of_heading
       test_unconnected_lowercase_5_letter_words # scores can get worse :-)
  s6 = test_sentence_of_lowercase_5_letter_words
  s7 = test_better_sentence_of_lowercase_5_letter_words
  s8 = test_profound_sentence_of_lowercase_5_letter_words
  assert_equal(true, sorted?([s0,s1,s2,s3,s4,s5,s6,s7,s8]), 'not sorted!')
end

def assert_equal(expected, actual, msg = '')
  if !(expected === actual)
    puts "ERROR:#{msg}"
    puts "expected: #{expected.inspect}"
    puts "  actual: #{actual.inspect}"
    exit(42)
  end
end

def assert_sums(expected, scores)
  scores.size.times do |i|
    assert_equal(expected[i], sum(scores[i]))
  end
end

#test_example_with_only_3_squads
#test_scores_increase_as_cookies_are_unlocked
#print_scores
