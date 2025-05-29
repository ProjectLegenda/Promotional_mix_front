
from django.db import models
from .projects import projects

class mmm(models.Model):

    agg_chnl_list= models.TextField()
    segmentation_type= models.TextField()
    parameters= models.TextField()
    rawdata_unscaled_dict = models.TextField()
    rawdata_scaled_dict = models.TextField()
    digital_gsk_impute = models.TextField()
    average_pirce_orig = models.TextField()
    average_pirce_agg= models.TextField()
    average_count_orig= models.TextField()
    average_count_agg= models.TextField()
    total_cost_sales_ratio= models.TextField()
    cost_dist= models.TextField()
    line_trend_dist= models.TextField()
    extra_features_1= models.TextField()
    r_square_mape= models.TextField()
    channel_contribution= models.TextField() 
    base_contribution= models.TextField()
    roi_mroi= models.TextField()
    mmm= models.TextField()
    last = models.BooleanField(default=1)
    projects = models.ForeignKey(projects, on_delete=models.CASCADE)