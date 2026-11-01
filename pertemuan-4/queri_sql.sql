select 
    date(fo.order_purchase_timestamp) as order_date,
    COUNT(distinct fo.order_id) as total_orders,
    count (distinct fo.customer_id) as total_customer,
    COUNT(foi.order_item_id) as total_item,
    SUM(foi.price ) as total_revenue
from fact_orders fo 
left join fact_order_items foi on fo.order_id = foi.order_id 
where fo.order_status not in ('unavailable', 'canceled')
group by date(fo.order_purchase_timestamp)
order  by order_date desc  

select distinct fo.order_status
from fact_orders fo 

select 
    date(fo.order_purchase_timestamp) as order_date,
    COUNT(distinct fo.order_id) as total_orders,
    count (distinct fo.customer_id) as total_customer,
    COUNT(foi.order_item_id) as total_item,
    SUM(foi.price ) as total_revenue
from fact_orders fo 
left join fact_order_items foi on fo.order_id = foi.order_id 
where fo.order_status not in ('unavailable', 'canceled')
group by date(fo.order_purchase_timestamp)
order  by order_date desc  

SELECT 
    COUNT(foi.order_id) as total_order,
    dp.product_category_name, 
FROM fact_order_items foi 
INNER JOIN fact_orders fo ON foi.order_id = fo.order_id 
LEFT JOIN dim_products dp ON foi.product_id = dp.product_id
group by foi.product_id, dp.product_category_name 
order by total_order desc 

select
	fo.customer_id,
	COUNT(fo.order_status = 'delivered')
from fact_orders fo 
group by fo.customer_id 
HAVING COUNT(fo.customer_id) > 1;


