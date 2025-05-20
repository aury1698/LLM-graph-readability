# GD97

This directory contains the old original graph files from Helen Purchase's paper.

Sara was able to obtain those from Helen Purchase, which is a great surprise. After all, the paper was published in 1997.
Additionally, we also received the practise graphs, which were not published in the paper.

We received these files on May 16, 2025. At this point we had already recreated the graphs by visual inspection.
The original graph files now serve as a reference and we can use them to
create the practise graphs and the original graphs more faithfully.

## Graph files

The graph files appear to be in the GraphEd format, which is a format used by the GraphEd software.
Sara found out that GraphEd is a long-discontinued software from the University of Passau, Germany.

> Their website (pardon the links from the wayback machine: https://web.archive.org/web/20060204014540/https://www.infosun.fmi.uni-passau.de/GraphEd/) doesn't say much, and the format seems to have been documented in this paper (?): https://web.archive.org/web/20010926124025/http://citeseer.nj.nec.com/140899.html whose PDF is unfortunately not cached in the wayback machine. I did not find any other traces of existence of this document on the web, we only have the abstract.
However, I did find what remains of GraphEd on a github repository: https://github.com/GunterMueller/UNI_PASSAU_FMI_Graph_Drawing?tab=readme-ov-file

## Helen Purchase's email response to Sara

To document the origin of the files, here is a copy of the email from Helen Purchase in response to Sara.

<blockquote>
Dear Sara,

How nice to hear from you! I must confess that I had two reactions to your email: sincere delight that you are looking at replicating this experiment, and awkward embarrassment about it.


I have learned so much in the past 30years, and looking back on my early publications, I cringe at them. The field has grown so much since then, and we know so much more - I would run this experiment very differently if I were to do it now. I actually have a box on my shelf with all my papers in hard copy, in order of publication; it shows the progress of what I have learned and how my research has developed over time. While I cringe at my early publications, it is somewhat reassuring that the quality of my work has improved over time!


Apologies for the delay in responding - I have been digging out some old DVDs, tracking down a DVD drive, and trying to see what I can find for you. It took a while (again, I blush at my sloppy experimental resources curation;  would be much more careful now).


In answer to your questions:


* I attach a folder that includes all the experimental graph drawings as well as the practice drawings. They are in a format that I don't know anymore (.g) and so I can't open them. And I can't remember why we chose those particular practice drawings. If you can look at them, you may find that they have been chosen from the experimental set, or are minor  variations. I'm afraid that I don't remember why we had the zz.g drawing - it is not referred to in the paper. I think it may have been a random layout that was included for comparison - but that we didn't use the data from it at the end after all.


* the filler task was:
Three students, Anne, Brian and Mary have all got their marks from an assignment.  
The surnames of these students are Brown, White and Green,
and their marks are 42, 64 and 56 (not necessarily in order).
Mary's mark was less than Miss Brown's by a factor of 25%,
and the child whose surname is White got a mark of 64. 



It is really interesting that you are looking at replication. I have a PhD student starting next month who will be working on just this: critique and replication of experiments to see what we can learn about changing and different methodologies.  I am particularly interested in how different methodologies might give different results, yet we (as a research community) are happy to accept and cite the results of a single experiment. We will, of course, be starting with my own experiments - so please do keep me informed as to how you get on with this one: I am very interested!


best wishes and good luck,

Helen
</blockquote>

## Aurora's conversion script

Aurora developed a new script (`convert_graphed_to_yed.py`) that parses the original `.g` files and generates a yEd-compatible GraphML file. This script preserves:

- the exact node positions as specified in the GraphEd file,
- the original edge bends (so that the orthogonal or polyline edge routing is maintained),
- and the node labels and shapes.
