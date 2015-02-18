#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0x9a31bb74, "module_layout" },
	{ 0x609f1c7e, "synchronize_net" },
	{ 0x5cd9dbb5, "kmalloc_caches" },
	{ 0x15692c87, "param_ops_int" },
	{ 0xf78d04ab, "netlink_register_notifier" },
	{ 0x716e7f27, "sock_release" },
	{ 0xc01cf848, "_raw_read_lock" },
	{ 0x546cd026, "icmp_send" },
	{ 0x38b6b4de, "dev_get_by_name" },
	{ 0x2124474, "ip_send_check" },
	{ 0xf338d4c3, "netlink_unregister_notifier" },
	{ 0x6b0211e7, "nf_register_hook" },
	{ 0x91715312, "sprintf" },
	{ 0x3d44f3a6, "in_dev_finish_destroy" },
	{ 0x7d11c268, "jiffies" },
	{ 0x6c9f714d, "skb_trim" },
	{ 0xe2d5255a, "strcmp" },
	{ 0x35b6b772, "param_ops_charp" },
	{ 0x27e1a049, "printk" },
	{ 0x8b6ece68, "proc_net_remove" },
	{ 0x2649054, "security_sock_rcv_skb" },
	{ 0x7f658e80, "_raw_write_lock" },
	{ 0x170baafa, "ip_route_me_harder" },
	{ 0xde794587, "dev_get_by_index" },
	{ 0x68aca4ad, "down" },
	{ 0x44c87265, "init_net" },
	{ 0x88a49dfb, "skb_copy_expand" },
	{ 0x28ce48ff, "__alloc_skb" },
	{ 0x8f7f1ef1, "netlink_broadcast" },
	{ 0xf0fdf6cb, "__stack_chk_fail" },
	{ 0x1ed94e8b, "kfree_skb" },
	{ 0x57a0725b, "create_proc_entry" },
	{ 0xbdfb6dbb, "__fentry__" },
	{ 0x6bdc92f6, "netlink_ack" },
	{ 0xd61adcbd, "kmem_cache_alloc_trace" },
	{ 0x99195078, "vsnprintf" },
	{ 0xf6ebc03b, "net_ratelimit" },
	{ 0x5c3edd59, "_raw_write_unlock_bh" },
	{ 0xd43b0634, "nf_unregister_hook" },
	{ 0xd814baf, "__netlink_kernel_create" },
	{ 0xfdee7d42, "_raw_read_lock_bh" },
	{ 0xf37260ab, "_raw_read_unlock_bh" },
	{ 0x37a0cba, "kfree" },
	{ 0x69acdf38, "memcpy" },
	{ 0x4845c423, "param_array_ops" },
	{ 0x71e3cecb, "up" },
	{ 0x32eeaded, "_raw_write_lock_bh" },
	{ 0xb0e602eb, "memmove" },
	{ 0x11f2fca, "skb_put" },
	{ 0x62f3f980, "sock_wfree" },
	{ 0xcb7d430e, "__nlmsg_put" },
	{ 0x108411ed, "__ip_select_ident" },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=";


MODULE_INFO(srcversion, "F779DB54A2169DEC997E049");
