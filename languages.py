#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import locale
import os

class LanguageManager:
    """Çok dilli destek yöneticisi"""

    def __init__(self):
        # 默认使用中文界面
        self.current_language = 'zh'
        self.translations = self.load_translations()

    def detect_system_language(self):
        """系统语言自动检测"""
        try:
            # 获取系统语言 (Python 3.15 兼容)
            try:
                system_locale = locale.getlocale()[0]
            except:
                # Fallback 旧方法
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    system_locale = locale.getdefaultlocale()[0]

            if system_locale:
                locale_lower = system_locale.lower()
                # 中文检测
                if (locale_lower.startswith(('zh', 'cn')) or
                    'chinese' in locale_lower or
                    '中文' in locale_lower):
                    return 'zh'
                # 土耳其语或阿塞拜疆语检测
                if (locale_lower.startswith(('tr', 'az')) or
                    'turkish' in locale_lower or
                    'türk' in locale_lower):
                    return 'tr'
                # 英语检测
                if locale_lower.startswith('en') or 'english' in locale_lower:
                    return 'en'

            # 默认使用中文
            return 'zh'
        except:
            return 'zh'

    def load_translations(self):
        """Çeviri dosyalarını yükle"""
        translations = {
            'zh': {
                # 通用
                'app_title': 'Warp 账户管理器',
                'yes': '是',
                'no': '否',
                'ok': '确定',
                'cancel': '取消',
                'close': '关闭',
                'error': '错误',
                'success': '成功',
                'warning': '警告',
                'info': '信息',

                # 按钮
                'proxy_start': '启动代理',
                'proxy_stop': '停止代理',
                'proxy_active': '代理已启用',
                'add_account': '添加账户',
                'refresh_limits': '刷新额度',
                'help': '帮助',
                'activate': '🟢 启用',
                'deactivate': '🔴 停用',
                'delete_account': '🗑️ 删除账户',
                'create_account': '🌐 创建账户',
                'add': '添加',
                'copy_javascript': '📋 复制 JavaScript 代码',
                'copied': '✅ 已复制！',
                'copy_error': '❌ 复制失败！',
                'open_certificate': '📁 打开证书文件',
                'installation_complete': '✅ 安装完成',

                # 表头
                'current': '当前',
                'email': '邮箱',
                'status': '状态',
                'limit': '额度',

                # 激活按钮文本
                'button_active': '已启用',
                'button_inactive': '未启用',
                'button_banned': '封禁',
                'button_start': '开始',
                'button_stop': '停止',

                # 状态消息
                'status_active': '启用',
                'status_banned': '封禁',
                'status_token_expired': '令牌已过期',
                'status_proxy_active': ' (代理已启用)',
                'status_error': '错误',
                'status_na': 'N/A',
                'status_not_updated': '未更新',
                'status_healthy': 'healthy',
                'status_unhealthy': 'unhealthy',
                'status_banned_key': 'banned',

                # 添加账户
                'add_account_title': '添加账户',
                'add_account_instruction': '在下方粘贴账户 JSON 数据：',
                'add_account_placeholder': '在此粘贴 JSON 数据...',
                'how_to_get_json': '❓ 如何获取 JSON 数据？',
                'how_to_get_json_close': '❌ 关闭',
                'json_info_title': '如何获取 JSON 数据？',

                # 账户添加对话框标签
                'tab_manual': '手动',
                'tab_auto': '自动',
                'manual_method_title': '手动添加 JSON',
                'auto_method_title': '使用 Chrome 扩展自动添加',

                # Chrome 扩展说明
                'chrome_extension_title': '🌐 Chrome 扩展',
                'chrome_extension_description': '可使用我们的 Chrome 扩展自动添加账户，方法更快更简单。',
                'chrome_extension_step_1': '<b>步骤 1：</b> 手动安装 Chrome 扩展',
                'chrome_extension_step_2': '<b>步骤 2：</b> 访问 Warp.dev 并创建新账户',
                'chrome_extension_step_3': '<b>步骤 3：</b> 创建账户后，在跳转页面点击扩展按钮',
                'chrome_extension_step_4': '<b>步骤 4：</b> 扩展会自动将账户添加到本程序',

                # 获取 JSON 步骤
                'step_1': '<b>步骤 1：</b> 打开 Warp 网站并登录',
                'step_2': '<b>步骤 2：</b> 打开浏览器开发者控制台（F12）',
                'step_3': '<b>步骤 3：</b> 切换到 Console 选项卡',
                'step_4': '<b>步骤 4：</b> 将下方 JavaScript 代码粘贴到控制台',
                'step_5': '<b>步骤 5：</b> 回车执行',
                'step_6': '<b>步骤 6：</b> 点击页面出现的按钮',
                'step_7': '<b>步骤 7：</b> 将复制的 JSON 粘贴到此处',

                # 帮助
                'help_title': '📖 Warp 账户管理器 - 使用指南',
                'help_what_is': '🎯 这个软件有什么用？',
                'help_what_is_content': '为了免费使用 Warp.dev 代码编辑器，你可以查看所创建账户之间的剩余额度，并通过“开始”按钮轻松切换。程序在每次操作中使用不同的 ID，避免被封禁。',
                'help_how_works': '⚙️ 工作原理',
                'help_how_works_content': '通过代理修改 Warp 编辑器的请求。使用你选择的账户信息和不同的用户 ID 执行操作。',
                'help_how_to_use': '📝 如何使用？',
                'help_how_to_use_content': '''<b>首次安装：</b><br>
由于通过代理工作，首次启动时需要将指定证书安装到计算机的受信任的根证书颁发机构中。完成指引后，打开 Warp 编辑器并登录任意账户。首次必须通过编辑器登录一个账户。<br><br>

<b>添加账户（两种方法）：</b><br>
<b>1. Chrome 扩展：</b> 在 Chrome 中安装我们的扩展。在 Warp.dev 创建账户后，跳转页面会出现扩展按钮，一键自动添加账户。<br>
<b>2. 手动方法：</b> 在创建账户页面按 F12 打开控制台，粘贴 JavaScript 代码并复制 JSON 添加到程序。<br><br>

<b>Chrome 扩展安装：</b><br>
手动安装 Chrome 扩展。扩展安装后，会在 warp.dev/logged_in/remote 页面显示自动添加账户按钮；在普通的 logged_in 页面会显示刷新页面按钮。<br><br>

<b>使用：</b><br>
要使用你添加的账户，请先启用代理。启用后，点击某个账户的“开始”按钮将其设为激活，然后继续使用 Warp 编辑器。点击“刷新额度”可即时查看各账户额度。''',

                # 证书安装
                'cert_title': '🔒 需要安装代理证书',
                'cert_explanation': '''为确保 Warp 代理正常工作，需要将 mitmproxy 证书
添加到受信任的根证书颁发机构中。

此操作只需进行一次，不会影响系统安全。''',
                'cert_steps': '📋 安装步骤：',
                'cert_step_1': '<b>步骤 1：</b> 点击下方“打开证书文件”按钮',
                'cert_step_2': '<b>步骤 2：</b> 双击打开的文件',
                'cert_step_3': '<b>步骤 3：</b> 点击“安装证书...”按钮',
                'cert_step_4': '<b>步骤 4：</b> 选择“本地计算机”，点击“下一步”',
                'cert_step_5': '<b>步骤 5：</b> 选择“将所有证书放入下列存储”',
                'cert_step_6': '<b>步骤 6：</b> 点击“浏览”按钮',
                'cert_step_7': '<b>步骤 7：</b> 选择“受信任的根证书颁发机构”',
                'cert_step_8': '<b>步骤 8：</b> 点击“确定”和“下一步”',
                'cert_step_9': '<b>步骤 9：</b> 点击“完成”按钮',
                'cert_path': '证书文件：{}',

                # 自动证书安装
                'cert_creating': '🔒 正在创建证书...',
                'cert_created_success': '✅ 证书文件创建成功',
                'cert_creation_failed': '❌ 证书创建失败',
                'cert_installing': '🔒 正在检查证书安装...',
                'cert_installed_success': '✅ 证书已自动安装',
                'cert_install_failed': '❌ 证书安装失败 —— 可能需要管理员权限',
                'cert_install_error': '❌ 证书安装错误：{}',

                # 手动证书安装对话框
                'cert_manual_title': '🔒 需要手动安装证书',
                'cert_manual_explanation': '''自动安装证书失败。

你需要手动安装证书。此操作只需进行一次，不会影响系统安全。''',
                'cert_manual_path': '证书文件位置：',
                'cert_manual_steps': '''<b>手动安装步骤：</b><br><br>
<b>1.</b> 前往上方文件路径<br>
<b>2.</b> 双击 <code>mitmproxy-ca-cert.cer</code> 文件<br>
<b>3.</b> 点击“安装证书...”按钮<br>
<b>4.</b> 选择“本地计算机”，点击“下一步”<br>
<b>5.</b> 选择“将所有证书放入下列存储”<br>
<b>6.</b> 点击“浏览” → 选择“受信任的根证书颁发机构”<br>
<b>7.</b> 点击“确定” → “下一步” → “完成”''',
                'cert_open_folder': '📁 打开证书文件夹',
                'cert_manual_complete': '✅ 我已完成安装',

                # 消息
                'account_added_success': '账户添加成功',
                'no_accounts_to_update': '没有可更新的账户',
                'updating_limits': '正在更新额度...',
                'processing_account': '正在处理：{}',
                'refreshing_token': '正在刷新令牌：{}',
                'accounts_updated': '已更新 {} 个账户',
                'proxy_starting': '正在启动代理...',
                'proxy_configuring': '正在配置 Windows 代理设置...',
                'proxy_started': '代理已启动：{}',
                'proxy_stopped': '代理已停止',
                'proxy_starting_account': '正在启动代理并激活 {}...',
                'activating_account': '正在激活账户：{}...',
                'token_refreshing': '正在刷新令牌：{}',
                'proxy_started_account_activated': '代理已启动并已激活 {}',
                'windows_proxy_config_failed': 'Windows 代理设置配置失败',
                'mitmproxy_start_failed': 'Mitmproxy 启动失败 - 请检查 8080 端口',
                'proxy_start_error': '代理启动错误：{}',
                'proxy_stop_error': '代理停止错误：{}',
                'account_not_found': '未找到账户',
                'account_banned_cannot_activate': '{} 账户已被封禁，无法激活',
                'account_activation_error': '账户激活错误：{}',
                'token_refresh_in_progress': '正在刷新令牌，请稍候...',
                'token_refresh_error': '令牌刷新错误：{}',
                'account_activated': '{} 账户已激活',
                'account_activation_failed': '账户激活失败',
                'proxy_unexpected_stop': '代理意外停止',
                'account_deactivated': '{} 账户已停用',
                'account_deleted': '已删除 {} 账户',
                'token_renewed': '{} 令牌已更新',
                'account_banned_detected': '⛔ 检测到 {} 账户被封禁！',
                'token_renewal_progress': '🔄 已更新 {}/{} 个令牌',

                # 错误消息
                'invalid_json': '无效的 JSON 格式',
                'email_not_found': '未找到邮箱',
                'certificate_not_found': '未找到证书文件！',
                'file_open_error': '文件打开错误：{}',
                'proxy_start_failed': '无法启动代理 - 请检查 8080 端口',
                'proxy_config_failed': '无法配置 Windows 代理设置',
                'token_refresh_failed': '无法更新 {} 的令牌',
                'account_delete_failed': '无法删除账户',
                'proxy_unexpected_stop': '⚠️ 代理意外停止',
                'enable_proxy_first': '请先启动代理以激活账户',
                'limit_info_failed': '无法获取额度信息',
                'token_renewal_failed': '⚠️ 无法更新 {} 的令牌',
                'token_check_error': '❌ 令牌检查错误',

                # 确认消息
                'delete_account_confirm': '确定要删除“{}”账户吗？\n\n此操作不可撤销！',

                # 状态栏消息
                'default_status': '启用代理并点击账户上的开始按钮即可开始使用。',
                'default_status_debug': '启用代理并点击账户上的开始按钮即可开始使用。（调试模式已启用）',

                # 调试与控制台消息
                'stylesheet_load_error': '样式表加载失败：{}',
                'health_update_error': '健康状态更新错误：{}',
                'token_update_error': '令牌更新错误：{}',
                'account_update_error': '账户更新错误：{}',
                'active_account_set_error': '设置激活账户错误：{}',
                'active_account_clear_error': '清除激活账户错误：{}',
                'account_delete_error': '删除账户错误：{}',
                'limit_info_update_error': '额度信息更新错误：{}',
            },

            'tr': {
                # Genel
                'app_title': 'Warp Hesap Yöneticisi',
                'yes': 'Evet',
                'no': 'Hayır',
                'ok': 'Tamam',
                'cancel': 'İptal',
                'close': 'Kapat',
                'error': 'Hata',
                'success': 'Başarılı',
                'warning': 'Uyarı',
                'info': 'Bilgi',

                # Butonlar
                'proxy_start': 'Proxy Başlat',
                'proxy_stop': 'Proxy Durdur',
                'proxy_active': 'Proxy Aktif',
                'add_account': 'Hesap Ekle',
                'refresh_limits': 'Limitleri Yenile',
                'help': 'Yardım',
                'activate': '🟢 Aktif Et',
                'deactivate': '🔴 Deaktif Et',
                'delete_account': '🗑️ Hesabı Sil',
                'create_account': '🌐 Hesap Oluştur',
                'add': 'Ekle',
                'copy_javascript': '📋 JavaScript Kodunu Kopyala',
                'copied': '✅ Kopyalandı!',
                'copy_error': '❌ Hata!',
                'open_certificate': '📁 Sertifika Dosyasını Aç',
                'installation_complete': '✅ Kurulumu Tamamladım',

                # Tablo başlıkları
                'current': 'Güncel',
                'email': 'Email',
                'status': 'Durum',
                'limit': 'Limit',

                # Aktivasyon buton metinleri
                'button_active': 'AKTİF',
                'button_inactive': 'PASİF',
                'button_banned': 'BAN',
                'button_start': 'Başlat',
                'button_stop': 'Durdur',

                # Durum mesajları
                'status_active': 'Aktif',
                'status_banned': 'BAN',
                'status_token_expired': 'Token Süresi Dolmuş',
                'status_proxy_active': ' (Proxy Aktif)',
                'status_error': 'Hata',
                'status_na': 'N/A',
                'status_not_updated': 'Güncellenmedi',
                'status_healthy': 'healthy',
                'status_unhealthy': 'unhealthy',
                'status_banned_key': 'banned',

                # Hesap ekleme
                'add_account_title': 'Hesap Ekle',
                'add_account_instruction': 'Hesap JSON verilerini aşağıya yapıştırın:',
                'add_account_placeholder': 'JSON verilerini buraya yapıştırın...',
                'how_to_get_json': '❓ JSON bilgilerini nasıl alırım?',
                'how_to_get_json_close': '❌ Kapat',
                'json_info_title': 'JSON Bilgilerini Nasıl Alırım?',

                # Hesap ekleme diyalogu tabları
                'tab_manual': 'Manuel',
                'tab_auto': 'Otomatik',
                'manual_method_title': 'Manuel JSON Ekleme',
                'auto_method_title': 'Chrome Eklentisi ile Otomatik Ekleme',

                # Chrome eklentisi açıklaması
                'chrome_extension_title': '🌐 Chrome Eklentisi',
                'chrome_extension_description': 'Chrome eklentimizi kullanarak hesaplarınızı otomatik olarak ekleyebilirsiniz. Bu yöntem daha hızlı ve kolaydır.',
                'chrome_extension_step_1': '<b>Adım 1:</b> Chrome eklentisini manuel olarak yükleyin',
                'chrome_extension_step_2': '<b>Adım 2:</b> Warp.dev sitesine gidin ve yeni hesap oluşturun',
                'chrome_extension_step_3': '<b>Adım 3:</b> Hesap oluşturduktan sonra yönlendirilen sayfada eklenti butonuna tıklayın',
                'chrome_extension_step_4': '<b>Adım 4:</b> Eklenti hesabı otomatik olarak bu programa ekleyecektir',

                # JSON alma adımları
                'step_1': '<b>Adım 1:</b> Warp web sitesine gidin ve giriş yapın',
                'step_2': '<b>Adım 2:</b> Tarayıcı geliştirici konsolunu açın (F12)',
                'step_3': '<b>Adım 3:</b> Console sekmesine gidin',
                'step_4': '<b>Adım 4:</b> Aşağıdaki JavaScript kodunu konsola yapıştırın',
                'step_5': '<b>Adım 5:</b> Enter tuşuna basın',
                'step_6': '<b>Adım 6:</b> Sayfada çıkan butona tıklayın',
                'step_7': '<b>Adım 7:</b> Kopyalanan JSON\'u buraya yapıştırın',

                # Yardım
                'help_title': '📖 Warp Hesap Yöneticisi - Kullanım Kılavuzu',
                'help_what_is': '🎯 Bu Yazılım Ne İşe Yarar?',
                'help_what_is_content': 'Warp.dev kod editörünü ücretsiz şekilde kullanabilmek için oluşturacağınız hesaplar arasında kalan limitlerinizi görebilir ve kolayca başlat butonuyla geçiş yapabilirsiniz. Her işleminizde farklı ID kullanarak banlanmanızı engeller.',
                'help_how_works': '⚙️ Nasıl Çalışır?',
                'help_how_works_content': 'Proxy kullanarak Warp editörünün yaptığı istekleri değiştirir. Seçtiğiniz hesabın bilgilerini ve farklı kullanıcı ID\'lerini kullanarak işlemleri gerçekleştirir.',
                'help_how_to_use': '📝 Nasıl Kullanılır?',
                'help_how_to_use_content': '''<b>İlk Kurulum:</b><br>
Proxy ile çalıştığı için ilk açılışta size belirtilen sertifikayı bilgisayarınızda güvenilen kök sertifikası alanında kurmanız beklenir. Talimatları tamamladıktan sonra Warp editörünü açarak herhangi bir hesaba giriş yaparsınız. İlk başta editör üzerinden bir hesaba giriş yapmanız zorunludur.<br><br>

<b>Hesap Ekleme (2 Yöntem):</b><br>
<b>1. Chrome Eklentisi:</b> Eklentimizi Chrome'a kurun. Warp.dev'de hesap oluşturduktan sonra yönlendirilen sayfada eklenti butonu belirir, tek tıkla hesap otomatik eklenir.<br>
<b>2. Manuel Yöntem:</b> Hesap oluşturma sayfasında F12 ile konsolu açın, JavaScript kodunu yapıştırın ve JSON'u kopyalayıp programa ekleyin.<br><br>

<b>Chrome Eklentisi Kurulumu:</b><br>
Chrome eklentisini manuel olarak yükleyin. Eklenti kurulduğunda, warp.dev/logged_in/remote sayfalarında otomatik hesap ekleme butonu görünür. Normal logged_in sayfalarında ise sayfa yenileme butonu belirir.<br><br>

<b>Kullanım:</b><br>
Yazılım üzerine eklediğiniz hesapları kullanabilmek için Proxy\'yi etkinleştirirsiniz. Etkinleştirme işleminden sonra hesaplarınızdan birine başlat butonuna tıklayarak aktif edebilir ve Warp editörünü kullanmaya devam edebilirsiniz. "Limitleri Yenile" butonu ile hesaplarınız arasındaki limitleri anlık görebilirsiniz.''',

                # Sertifika kurulumu
                'cert_title': '🔒 Proxy Sertifikası Kurulumu Gerekli',
                'cert_explanation': '''Warp Proxy'nin düzgün çalışması için mitmproxy sertifikasının
güvenilen kök sertifika yetkilileri arasına eklenmesi gerekiyor.

Bu işlem sadece bir kez yapılır ve sistem güvenliğinizi etkilemez.''',
                'cert_steps': '📋 Kurulum Adımları:',
                'cert_step_1': '<b>Adım 1:</b> Aşağıdaki "Sertifika Dosyasını Aç" butonuna tıklayın',
                'cert_step_2': '<b>Adım 2:</b> Açılan dosyaya çift tıklayın',
                'cert_step_3': '<b>Adım 3:</b> "Sertifika Yükle..." butonuna tıklayın',
                'cert_step_4': '<b>Adım 4:</b> "Yerel Makine" seçin ve "İleri" butonuna tıklayın',
                'cert_step_5': '<b>Adım 5:</b> "Tüm sertifikaları aşağıdaki depoya yerleştir" seçin',
                'cert_step_6': '<b>Adım 6:</b> "Gözat" butonuna tıklayın',
                'cert_step_7': '<b>Adım 7:</b> "Güvenilen Kök Sertifika Yetkilileri" klasörünü seçin',
                'cert_step_8': '<b>Adım 8:</b> "Tamam" ve "İleri" butonlarına tıklayın',
                'cert_step_9': '<b>Adım 9:</b> "Son" butonuna tıklayın',
                'cert_path': 'Sertifika dosyası: {}',

                # Otomatik sertifika kurulumu
                'cert_creating': '🔒 Sertifika oluşturuluyor...',
                'cert_created_success': '✅ Sertifika dosyası başarıyla oluşturuldu',
                'cert_creation_failed': '❌ Sertifika oluşturulamadı',
                'cert_installing': '🔒 Sertifika kurulumu kontrol ediliyor...',
                'cert_installed_success': '✅ Sertifika otomatik kuruldu',
                'cert_install_failed': '❌ Sertifika kurulumu başarısız - Yönetici yetkisi gerekebilir',
                'cert_install_error': '❌ Sertifika kurulum hatası: {}',

                # Manuel sertifika kurulum dialogu
                'cert_manual_title': '🔒 Manuel Sertifika Kurulumu Gerekli',
                'cert_manual_explanation': '''Otomatik sertifika kurulumu başarısız oldu.

Sertifikayı manuel olarak kurmanız gerekiyor. Bu işlem sadece bir kez yapılır ve sistem güvenliğinizi etkilemez.''',
                'cert_manual_path': 'Sertifika dosyası konumu:',
                'cert_manual_steps': '''<b>Manuel Kurulum Adımları:</b><br><br>
<b>1.</b> Yukarıdaki dosya yoluna gidin<br>
<b>2.</b> <code>mitmproxy-ca-cert.cer</code> dosyasına çift tıklayın<br>
<b>3.</b> "Sertifika Yükle..." butonuna tıklayın<br>
<b>4.</b> "Yerel Makine" seçin ve "İleri" tıklayın<br>
<b>5.</b> "Tüm sertifikaları aşağıdaki depoya yerleştir" seçin<br>
<b>6.</b> "Gözat" → "Güvenilen Kök Sertifika Yetkilileri" seçin<br>
<b>7.</b> "Tamam" → "İleri" → "Son" tıklayın''',
                'cert_open_folder': '📁 Sertifika Klasörünü Aç',
                'cert_manual_complete': '✅ Kurulumu Tamamladım',

                # Mesajlar
                'account_added_success': 'Hesap başarıyla eklendi',
                'no_accounts_to_update': 'Güncellenecek hesap bulunamadı',
                'updating_limits': 'Limitler güncelleniyor...',
                'processing_account': 'İşleniyor: {}',
                'refreshing_token': 'Token yenileniyor: {}',
                'accounts_updated': '{} hesap güncellendi',
                'proxy_starting': 'Proxy başlatılıyor...',
                'proxy_configuring': 'Windows proxy ayarları yapılandırılıyor...',
                'proxy_started': 'Proxy başlatıldı: {}',
                'proxy_stopped': 'Proxy durduruldu',
                'proxy_starting_account': 'Proxy başlatılıyor ve {} aktif ediliyor...',
                'activating_account': 'Hesap aktif ediliyor: {}...',
                'token_refreshing': 'Token yenileniyor: {}',
                'proxy_started_account_activated': 'Proxy başlatıldı ve {} aktif edildi',
                'windows_proxy_config_failed': 'Windows proxy ayarları yapılandırılamadı',
                'mitmproxy_start_failed': 'Mitmproxy başlatılamadı - Port 8080 kontrol edin',
                'proxy_start_error': 'Proxy başlatma hatası: {}',
                'proxy_stop_error': 'Proxy durdurma hatası: {}',
                'account_not_found': 'Hesap bulunamadı',
                'account_banned_cannot_activate': '{} hesabı banlanmış - aktif edilemez',
                'account_activation_error': 'Aktif etme hatası: {}',
                'token_refresh_in_progress': 'Token yenileme devam ediyor, lütfen bekleyin...',
                'token_refresh_error': 'Token yenileme hatası: {}',
                'account_activated': '{} hesabı aktif edildi',
                'account_activation_failed': 'Hesap aktif edilemedi',
                'proxy_unexpected_stop': 'Proxy beklenmedik şekilde durduruldu',
                'account_activated': '{} hesabı aktif edildi',
                'account_deactivated': '{} hesabı deaktif edildi',
                'account_deleted': '{} hesabı silindi',
                'token_renewed': '{} tokeni yenilendi',
                'account_banned_detected': '⛔ {} hesabı banlandı!',
                'token_renewal_progress': '🔄 {}/{} token yenilendi',

                # Hata mesajları
                'invalid_json': 'Geçersiz JSON formatı',
                'email_not_found': 'Email bulunamadı',
                'account_not_found': 'Hesap bulunamadı',
                'certificate_not_found': 'Sertifika dosyası bulunamadı!',
                'file_open_error': 'Dosya açma hatası: {}',
                'proxy_start_failed': 'Proxy başlatılamadı - Port 8080 kontrol edin',
                'proxy_config_failed': 'Windows proxy ayarları yapılandırılamadı',
                'account_banned_cannot_activate': '{} hesabı banlanmış - aktif edilemez',
                'token_refresh_failed': '{} tokeni yenilenemedi',
                'account_delete_failed': 'Hesap silinemedi',
                'proxy_unexpected_stop': '⚠️ Proxy beklenmedik şekilde durduruldu',
                'enable_proxy_first': 'Hesap aktif etmek için önce proxy\'yi başlatın',
                'limit_info_failed': 'Limit bilgisi alınamadı',
                'token_renewal_failed': '⚠️ {} token yenilenemedi',
                'token_check_error': '❌ Token kontrol hatası',

                # Onay mesajları
                'delete_account_confirm': '\'{}\' hesabını silmek istediğinizden emin misiniz?\n\nBu işlem geri alınamaz!',

                # Durum çubuğu mesajları
                'default_status': 'Proxy Etkinleştirip başlat butonuna tıklayarak kullanmaya başlayabilirsiniz.',
                'default_status_debug': 'Proxy Etkinleştirip başlat butonuna tıklayarak kullanmaya başlayabilirsiniz. (Debug Modu Aktif)',

                # Debug ve konsol mesajları (bunlar değişmeyebilir ama tutarlılık için)
                'stylesheet_load_error': 'Stil dosyası yüklenemedi: {}',
                'health_update_error': 'Sağlık durumu güncelleme hatası: {}',
                'token_update_error': 'Token güncelleme hatası: {}',
                'account_update_error': 'Hesap güncelleme hatası: {}',
                'active_account_set_error': 'Aktif hesap ayarlama hatası: {}',
                'active_account_clear_error': 'Aktif hesap temizleme hatası: {}',
                'account_delete_error': 'Hesap silme hatası: {}',
                'limit_info_update_error': 'Limit bilgisi güncelleme hatası: {}',


            },

            'en': {
                # General
                'app_title': 'Warp Account Manager',
                'yes': 'Yes',
                'no': 'No',
                'ok': 'OK',
                'cancel': 'Cancel',
                'close': 'Close',
                'error': 'Error',
                'success': 'Success',
                'warning': 'Warning',
                'info': 'Info',

                # Buttons
                'proxy_start': 'Start Proxy',
                'proxy_stop': 'Stop Proxy',
                'proxy_active': 'Proxy Active',
                'add_account': 'Add Account',
                'refresh_limits': 'Refresh Limits',
                'help': 'Help',
                'activate': '🟢 Activate',
                'deactivate': '🔴 Deactivate',
                'delete_account': '🗑️ Delete Account',
                'create_account': '🌐 Create Account',
                'add': 'Add',
                'copy_javascript': '📋 Copy JavaScript Code',
                'copied': '✅ Copied!',
                'copy_error': '❌ Error!',
                'open_certificate': '📁 Open Certificate File',
                'installation_complete': '✅ Installation Complete',

                # Table headers
                'current': 'Current',
                'email': 'Email',
                'status': 'Status',
                'limit': 'Limit',

                # Activation button texts
                'button_active': 'ACTIVE',
                'button_inactive': 'INACTIVE',
                'button_banned': 'BAN',
                'button_start': 'Start',
                'button_stop': 'Stop',

                # Status messages
                'status_active': 'Active',
                'status_banned': 'BAN',
                'status_token_expired': 'Token Expired',
                'status_proxy_active': ' (Proxy Active)',
                'status_error': 'Error',
                'status_na': 'N/A',
                'status_not_updated': 'Not Updated',
                'status_healthy': 'healthy',
                'status_unhealthy': 'unhealthy',
                'status_banned_key': 'banned',

                # Add account
                'add_account_title': 'Add Account',
                'add_account_instruction': 'Paste account JSON data below:',
                'add_account_placeholder': 'Paste JSON data here...',
                'how_to_get_json': '❓ How to get JSON data?',
                'how_to_get_json_close': '❌ Close',
                'json_info_title': 'How to Get JSON Data?',

                # Add account dialog tabs
                'tab_manual': 'Manual',
                'tab_auto': 'Automatic',
                'manual_method_title': 'Manual JSON Addition',
                'auto_method_title': 'Automatic Addition with Chrome Extension',

                # Chrome extension description
                'chrome_extension_title': '🌐 Chrome Extension',
                'chrome_extension_description': 'You can automatically add your accounts using our Chrome extension. This method is faster and easier.',
                'chrome_extension_step_1': '<b>Step 1:</b> Manually install the Chrome extension',
                'chrome_extension_step_2': '<b>Step 2:</b> Go to Warp.dev and create a new account',
                'chrome_extension_step_3': '<b>Step 3:</b> After creating account, click the extension button on the redirected page',
                'chrome_extension_step_4': '<b>Step 4:</b> Extension will automatically add the account to this program',

                # JSON extraction steps
                'step_1': '<b>Step 1:</b> Go to Warp website and login',
                'step_2': '<b>Step 2:</b> Open browser developer console (F12)',
                'step_3': '<b>Step 3:</b> Go to Console tab',
                'step_4': '<b>Step 4:</b> Paste the JavaScript code below into console',
                'step_5': '<b>Step 5:</b> Press Enter',
                'step_6': '<b>Step 6:</b> Click the button that appears on the page',
                'step_7': '<b>Step 7:</b> Paste the copied JSON here',

                # Help
                'help_title': '📖 Warp Account Manager - User Guide',
                'help_what_is': '🎯 What Does This Software Do?',
                'help_what_is_content': 'You can view remaining limits between accounts you create to use Warp.dev code editor for free and easily switch between them by clicking the start button. It prevents you from getting banned by using different IDs for each operation.',
                'help_how_works': '⚙️ How Does It Work?',
                'help_how_works_content': 'It modifies requests made by Warp editor using proxy. It performs operations using the information of the account you selected and different user IDs.',
                'help_how_to_use': '📝 How to Use?',
                'help_how_to_use_content': '''<b>Initial Setup:</b><br>
Since it works with proxy, you are expected to install the specified certificate in the trusted root certificate area on your computer at first launch. After completing the instructions, open Warp editor and login to any account. You must login to an account through the editor first.<br><br>

<b>Adding Accounts (2 Methods):</b><br>
<b>1. Chrome Extension:</b> Install our extension to Chrome. After creating account on Warp.dev, extension button appears on redirected page, one-click adds account automatically.<br>
<b>2. Manual Method:</b> On account creation page, open console with F12, paste JavaScript code and copy JSON to add to program.<br><br>

<b>Chrome Extension Installation:</b><br>
Manually install the Chrome extension. When extension is installed, automatic account addition button appears on warp.dev/logged_in/remote pages. On normal logged_in pages, a page refresh button appears.<br><br>

<b>Usage:</b><br>
To use the accounts you added to the software, you activate the Proxy. After the activation process, you can activate one of your accounts by clicking the start button and continue using the Warp editor. You can instantly see the limits between your accounts with the "Refresh Limits" button.''',

                # Certificate installation
                'cert_title': '🔒 Proxy Certificate Installation Required',
                'cert_explanation': '''For Warp Proxy to work properly, mitmproxy certificate needs to be added to trusted root certificate authorities.

This process is done only once and does not affect your system security.''',
                'cert_steps': '📋 Installation Steps:',
                'cert_step_1': '<b>Step 1:</b> Click the "Open Certificate File" button below',
                'cert_step_2': '<b>Step 2:</b> Double-click the opened file',
                'cert_step_3': '<b>Step 3:</b> Click "Install Certificate..." button',
                'cert_step_4': '<b>Step 4:</b> Select "Local Machine" and click "Next"',
                'cert_step_5': '<b>Step 5:</b> Select "Place all certificates in the following store"',
                'cert_step_6': '<b>Step 6:</b> Click "Browse" button',
                'cert_step_7': '<b>Step 7:</b> Select "Trusted Root Certification Authorities" folder',
                'cert_step_8': '<b>Step 8:</b> Click "OK" and "Next" buttons',
                'cert_step_9': '<b>Step 9:</b> Click "Finish" button',
                'cert_path': 'Certificate file: {}',

                # Automatic certificate installation
                'cert_creating': '🔒 Creating certificate...',
                'cert_created_success': '✅ Certificate file created successfully',
                'cert_creation_failed': '❌ Certificate creation failed',
                'cert_installing': '🔒 Checking certificate installation...',
                'cert_installed_success': '✅ Certificate installed automatically',
                'cert_install_failed': '❌ Certificate installation failed - Administrator privileges may be required',
                'cert_install_error': '❌ Certificate installation error: {}',

                # Manual certificate installation dialog
                'cert_manual_title': '🔒 Manual Certificate Installation Required',
                'cert_manual_explanation': '''Automatic certificate installation failed.

You need to install the certificate manually. This process is done only once and does not affect your system security.''',
                'cert_manual_path': 'Certificate file location:',
                'cert_manual_steps': '''<b>Manual Installation Steps:</b><br><br>
<b>1.</b> Go to the file path above<br>
<b>2.</b> Double-click the <code>mitmproxy-ca-cert.cer</code> file<br>
<b>3.</b> Click "Install Certificate..." button<br>
<b>4.</b> Select "Local Machine" and click "Next"<br>
<b>5.</b> Select "Place all certificates in the following store"<br>
<b>6.</b> Click "Browse" → Select "Trusted Root Certification Authorities"<br>
<b>7.</b> Click "OK" → "Next" → "Finish"''',
                'cert_open_folder': '📁 Open Certificate Folder',
                'cert_manual_complete': '✅ Installation Complete',

                # Messages
                'account_added_success': 'Account added successfully',
                'no_accounts_to_update': 'No accounts found to update',
                'updating_limits': 'Updating limits...',
                'processing_account': 'Processing: {}',
                'refreshing_token': 'Refreshing token: {}',
                'accounts_updated': '{} accounts updated',
                'proxy_starting': 'Starting proxy...',
                'proxy_configuring': 'Configuring Windows proxy settings...',
                'proxy_started': 'Proxy started: {}',
                'proxy_stopped': 'Proxy stopped',
                'proxy_starting_account': 'Starting proxy and activating {}...',
                'activating_account': 'Activating account: {}...',
                'token_refreshing': 'Refreshing token: {}',
                'proxy_started_account_activated': 'Proxy started and {} activated',
                'windows_proxy_config_failed': 'Windows proxy configuration failed',
                'mitmproxy_start_failed': 'Mitmproxy failed to start - Check port 8080',
                'proxy_start_error': 'Proxy start error: {}',
                'proxy_stop_error': 'Proxy stop error: {}',
                'account_not_found': 'Account not found',
                'account_banned_cannot_activate': '{} account is banned - cannot activate',
                'account_activation_error': 'Account activation error: {}',
                'token_refresh_in_progress': 'Token refresh in progress, please wait...',
                'token_refresh_error': 'Token refresh error: {}',
                'account_activated': '{} account activated',
                'account_activation_failed': 'Account activation failed',
                'proxy_unexpected_stop': 'Proxy stopped unexpectedly',
                'account_activated': '{} account activated',
                'account_deactivated': '{} account deactivated',
                'account_deleted': '{} account deleted',
                'token_renewed': '{} token renewed',
                'account_banned_detected': '⛔ {} account banned!',
                'token_renewal_progress': '🔄 {}/{} tokens renewed',

                # Error messages
                'invalid_json': 'Invalid JSON format',
                'email_not_found': 'Email not found',
                'account_not_found': 'Account not found',
                'certificate_not_found': 'Certificate file not found!',
                'file_open_error': 'File open error: {}',
                'proxy_start_failed': 'Proxy could not be started - Check port 8080',
                'proxy_config_failed': 'Windows proxy settings could not be configured',
                'account_banned_cannot_activate': '{} account is banned - cannot be activated',
                'token_refresh_failed': '{} token could not be renewed',
                'account_delete_failed': 'Account could not be deleted',
                'proxy_unexpected_stop': '⚠️ Proxy stopped unexpectedly',
                'enable_proxy_first': 'Start proxy first to activate account',
                'limit_info_failed': 'Could not get limit information',
                'token_renewal_failed': '⚠️ {} token could not be renewed',
                'token_check_error': '❌ Token check error',

                # Confirmation messages
                'delete_account_confirm': 'Are you sure you want to delete \'{}\' account?\n\nThis action cannot be undone!',

                # Status bar messages
                'default_status': 'Enable Proxy and click the start button on accounts to start using.',
                'default_status_debug': 'Enable Proxy and click the start button on accounts to start using. (Debug Mode Active)',

                # Debug and console messages (these might not change but for consistency)
                'stylesheet_load_error': 'Could not load stylesheet: {}',
                'health_update_error': 'Health status update error: {}',
                'token_update_error': 'Token update error: {}',
                'account_update_error': 'Account update error: {}',
                'active_account_set_error': 'Active account set error: {}',
                'active_account_clear_error': 'Active account clear error: {}',
                'account_delete_error': 'Account delete error: {}',
                'limit_info_update_error': 'Limit info update error: {}',


            }
        }

        return translations

    def get_text(self, key, *args):
        """获取翻译文本（带英文兜底）"""
        try:
            current = self.translations.get(self.current_language, {})
            text = current.get(key)
            if text is None:
                text = self.translations.get('en', {}).get(key, key)
            if args:
                return text.format(*args)
            return text
        except:
            return key

    def set_language(self, language_code):
        """设置语言，支持常见别名（如 zh-CN -> zh）"""
        if not language_code:
            return False
        code = str(language_code).lower().replace('-', '_')
        if code in ('zh_cn', 'zh_hans', 'zh'):
            target = 'zh'
        elif code in ('tr_tr', 'tr'):
            target = 'tr'
        elif code.startswith('en'):
            target = 'en'
        else:
            target = code if code in self.translations else None
        if target in self.translations:
            self.current_language = target
            return True
        return False

    def get_current_language(self):
        """Mevcut dili döndür"""
        return self.current_language

    def get_available_languages(self):
        """Kullanılabilir dilleri döndür"""
        return list(self.translations.keys())

# Global dil yöneticisi instance'ı
_language_manager = None

def get_language_manager():
    """Global dil yöneticisini al"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager

def _(key, *args):
    """Kısa çeviri fonksiyonu"""
    return get_language_manager().get_text(key, *args)
