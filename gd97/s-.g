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
WAWIN 0 42 855 759
SC 1578 1489
GR 32
$}
14 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2080 1728 $}"A"
 15 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2068 1728 1952 1728 1834 1786 $}""
 18 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2069 1735 1962 1816 $}""
;
15 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1824 1792 $}"E"
 16 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1812 1793 1643 1822 $}""
 18 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1835 1794 1940 1821 $}""
;
18 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1952 1824 $}"B"
 19 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1945 1836 1926 1875 $}""
 22 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1940 1828 1803 1883 $}""
 16 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1940 1824 1643 1824 $}""
 21 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1962 1829 2133 1914 $}""
;
16 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1632 1824 $}"F"
 20 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1641 1833 1910 2102 $}""
;
19 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1920 1888 $}"T"
 20 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1920 1903 1920 2096 $}""
 16 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1908 1885 1760 1856 1643 1826 $}""
;
22 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1792 1888 $}"C"
 23 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1803 1890 2068 1949 $}""
;
21 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2144 1920 $}"H"
 25 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2153 1910 2230 1833 $}""
;
20 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1920 2112 $}"G"
 22 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1912 2099 1799 1900 $}""
 21 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1929 2103 2134 1928 $}""
;
17 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1984 1664 $}"S"
 15 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1974 1671 1833 1784 $}""
 16 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1973 1668 1642 1819 $}""
 14 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1994 1670 2069 1721 $}""
;
23 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2080 1952 $}"N"
 24 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2069 1957 1962 2010 $}""
 18 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2070 1942 1961 1833 $}""
;
25 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2240 1824 $}"I"
 28 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2249 1814 2272 1792 2272 1583 $}""
 26 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2229 1816 2122 1735 $}""
;
24 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1952 2016 $}"O"
 22 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1942 2008 1801 1895 $}""
;
28 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2272 1568 $}"J"
;
26 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2112 1728 $}"P"
;
27 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 2208 1600 $}"Q"
 25 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2210 1615 2237 1808 $}""
 28 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2218 1594 2261 1573 $}""
 26 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 2199 1610 2120 1717 $}""
;
29 {$ NS 23 31 NTI 2 NFI 26 NLP 0 NEI 4 NLV 1 COL 1 NP 1632 1696 $}"R"
 27 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1643 1694 2196 1601 $}""
 28 {$ ETI 0 EFI 22 ELV 1 AL 8 AA 45 COL 3 EL 1643 1692 1920 1600 2260 1569 $}""
;
END
