GRAPH "" =  UNDIRECTED
{$
Font:	0	"courier-10"	"10"
Font:	1	"courier-bold-10"	"10 b"
Font:	2	"courier-italic-10"	"10 b"
Font:	3	"courier-12"	"12"
Font:	4	"courier-bold-12"	"12 b"
Font:	5	"courier-italic-12"	"12 b"
Font:	6	"courier-14"	"14"
Font:	7	"courier-bold-14"	"14 b"
Font:	8	"courier-italic-14"	"14 b"
Font:	9	"courier-18"	"18"
Font:	10	"courier-bold-18"	"18 b"
Font:	11	"courier-italic-18"	"18 b"
Font:	12	"courier-24"	"24"
Font:	13	"courier-bold-24"	"24 b"
Font:	14	"courier-italic-24"	"24 b"
Font:	15	"/usr/lib/fonts/fixedwidthfonts/cour.r.10"	"cour.r.10"
Font:	16	"/usr/lib/fonts/fixedwidthfonts/cour.b.10"	"cour.b.10"
Font:	17	"/usr/lib/fonts/fixedwidthfonts/cour.r.12"	"cour.r.12"
Font:	18	"/usr/lib/fonts/fixedwidthfonts/cour.b.12"	"cour.b.12"
Font:	19	"/usr/lib/fonts/fixedwidthfonts/cour.r.14"	"cour.r.14"
Font:	20	"/usr/lib/fonts/fixedwidthfonts/cour.b.14"	"cour.b.14"
Font:	21	"/usr/lib/fonts/fixedwidthfonts/cour.r.16"	"cour.r.16"
Font:	22	"/usr/lib/fonts/fixedwidthfonts/cour.b.16"	"cour.b.16"
Font:	23	"/usr/lib/fonts/fixedwidthfonts/cour.r.18"	"cour.r.18"
Font:	24	"/usr/lib/fonts/fixedwidthfonts/cour.b.18"	"cour.b.18"
Font:	25	"/usr/lib/fonts/fixedwidthfonts/cour.r.24"	"cour.r.24"
Font:	26	"/usr/lib/fonts/fixedwidthfonts/cour.b.24"	"cour.b.24"
Font:	27	"/usr/lib/fonts/fixedwidthfonts/serif.r.16"	"serif.r.16"
;
NodeType:	0	"#box"
NodeType:	1	"#double_box"
NodeType:	2	"#circle"
NodeType:	3	"#double_circle"
NodeType:	4	"#diamond"
NodeType:	5	"#double_diamond"
NodeType:	6	"#white"
NodeType:	7	"#black"
NodeType:	8	"sad_face.icon"
NodeType:	9	"happy_face.icon"
NodeType:	10	"searchers/move.icon"
NodeType:	11	"searchers/search.icon"
NodeType:	12	"searchers/nosearch.icon"
;
EdgeType:	0	"#solid"
EdgeType:	1	"#dashed"
EdgeType:	2	"#dotted"
EdgeType:	3	"#dashdotted"
EdgeType:	4	"#dashdotdotted"
EdgeType:	5	"#longdashed"
;
NSTYL "normal" [  NS 16 16 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 0 0 ]
NSTYL "gragra left side" [  NS 128 128 NTI 0 NFI 22 NLP 1 NEI 4 NLV 1 COL 10 NP 0 0 ]
NSTYL "gragra embed node" [  NS 32 32 NTI 4 NFI 22 NLP 0 NEI 1 NLV 1 COL 12 NP 0 0 ]
ESTYL "normal" [  ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 ]
ESTYL "gragra embed edge" [  ETI 2 EFI 22 ELV 1 AL 8 AA 45 COL 9 ]
DIR 0
GRAGRA 3 "[a-z_$]*""[A-Z][a-zA-Z_$]*" GEMBED "embedding" EMBMATCH 0
ELS 256 64

;
WA 4000 4000
WAWIN 0 21 855 759
SC 1662 1489
GR 16
$}
14 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1872 1728 $}"A"
 15 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1878 1740 1897 1779 $}""
 18 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1881 1735 1974 1816 $}""
;
15 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1904 1792 $}"E"
 16 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1900 1806 1888 1856 1911 1879 $}""
 18 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1914 1796 1973 1819 $}""
;
17 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1968 1760 $}"S"
 15 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1957 1765 1914 1786 $}""
 16 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1962 1773 1925 1874 $}""
 14 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1957 1756 1882 1731 $}""
;
18 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1984 1824 $}"B"
 19 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1980 1838 1971 1873 $}""
 22 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1994 1818 2037 1797 $}""
 16 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1975 1832 1928 1879 $}""
 21 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1994 1829 2016 1840 2041 1891 $}""
;
16 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1920 1888 $}"F"
 20 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1926 1900 1936 1920 2000 1920 2056 1849 $}""
;
22 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2048 1792 $}"C"
 23 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2048 1777 2048 1759 $}""
;
19 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1968 1888 $}"T"
 20 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1978 1882 2054 1844 $}""
 16 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1957 1888 1931 1888 $}""
;
21 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2048 1904 $}"H"
 25 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2059 1904 2085 1904 $}""
;
20 {$ NS 20 28 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2064 1840 $}"G"
 22 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2059 1827 2052 1805 $}""
 21 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2060 1853 2051 1889 $}""
;
23 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2048 1744 $}"N"
 24 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2059 1744 2160 1744 2132 1826 $}""
 18 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2039 1754 1992 1813 $}""
;
25 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2096 1904 $}"I"
 28 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2096 1889 2096 1871 $}""
 26 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2106 1909 2149 1930 $}""
;
26 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2160 1936 $}"P"
;
28 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2096 1856 $}"J"
;
24 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2128 1840 $}"O"
 22 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2119 1831 2080 1792 2059 1792 $}""
;
27 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2176 1872 $}"Q"
 25 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2165 1876 2106 1899 $}""
 28 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2165 1869 2106 1858 $}""
 26 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2172 1886 2163 1921 $}""
;
29 {$ NS 22 30 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2112 1776 $}"R"
 27 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2119 1787 2168 1860 $}""
 28 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2109 1790 2098 1841 $}""
;
END
