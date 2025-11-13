# wsd.r - dynamic tukeySEM for any number of Layout levels

pkgs <- c("readr", "dplyr", "tidyr", "lavaan", "semTools")
new <- pkgs[!(pkgs %in% installed.packages()[, "Package"])]
if(length(new)) install.packages(new)
lapply(pkgs, library, character.only = TRUE)

# Path to your CSV (update if needed)
#csv_file <- "error_rate_per_subject_type_-.csv"
# auro's version:
csv_file <- "error_per_subject_all_layouts.csv"

wide <- readr::read_csv(csv_file, show_col_types = FALSE)

rep_cols <- names(wide)[sapply(wide, is.numeric)]
if(length(rep_cols) == 0) stop("No numeric columns found in the CSV to compare.")

lavaan_data <- wide %>% select(all_of(rep_cols))

means <- colMeans(lavaan_data, na.rm = TRUE)
vars  <- apply(lavaan_data, 2, var, na.rm = TRUE)
ns    <- colSums(!is.na(lavaan_data))

ng <- length(rep_cols)

pairs <- t(combn(rep_cols, 2))
res_list <- vector("list", nrow(pairs))
for(k in seq_len(nrow(pairs))) {
    g1 <- pairs[k, 1]; g2 <- pairs[k, 2]
    out <- semTools::tukeySEM(
        m1 = means[g1], m2 = means[g2],
        var1 = vars[g1], var2 = vars[g2],
        n1 = ns[g1], n2 = ns[g2],
        ng = ng
    )

    res_list[[k]] <- data.frame(
        group1 = g1, group2 = g2,
        q = as.numeric(out[1]),
        df = as.numeric(out[2]),
        p = as.numeric(out[3]),
        stringsAsFactors = FALSE
    )
}

tukey_results <- do.call(rbind, res_list)

print(tukey_results)





