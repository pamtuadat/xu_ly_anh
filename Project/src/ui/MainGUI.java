package ui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.ButtonGroup;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButton;

@SuppressWarnings("serial")
public class MainGUI extends JFrame implements ActionListener {	
    private JRadioButton rdaXuLyAnh;
    private JRadioButton rdaTCA;
    private JButton btnChonAnh;
    private JButton btnThucHien;
    private JRadioButton rdaGamma;
    private JRadioButton rdaNega;
    private JRadioButton rdaLog;
    private JButton btnReset;
    private JPanel pnlSouth;
    private JLabel lblPath;
    private File file;
    private JPanel pnlCenter;
    private JLabel lblImage;  
    private JLabel lblResult;  
	private JLabel lblImageRes;
	private JButton btnExit;

    public MainGUI() {
        super("Xử lý ảnh");
        setGUI();
        setBounds(250, 100, 1000, 620);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setVisible(true);
    }

    public void setGUI() {
        JPanel pnlNorth = new JPanel();
        JLabel lblTitle = new JLabel("Xử lý ảnh cơ bản");
        lblTitle.setFont(new Font("Arial", Font.BOLD, 28));
        lblTitle.setForeground(Color.blue);
        pnlNorth.add(lblTitle);
        add(pnlNorth, BorderLayout.NORTH);

        JPanel pnlWest = new JPanel();
        pnlWest.setPreferredSize(new Dimension(200, 0));
        pnlWest.setBorder(BorderFactory.createTitledBorder(""));
        Box bxY = Box.createVerticalBox();
        Box bxWest = Box.createVerticalBox();

        // --- Chọn chức năng
        JPanel pnl = new JPanel();
        pnl.setBorder(BorderFactory.createTitledBorder("Chọn chức năng"));
        rdaXuLyAnh = new JRadioButton("Nhận diện biển số xe");
        rdaTCA = new JRadioButton("Nâng cao chất lượng ảnh");
        
        rdaXuLyAnh.addActionListener(this);
        rdaTCA.addActionListener(this);
        
        ButtonGroup btgCn = new ButtonGroup();
        btgCn.add(rdaTCA);
        btgCn.add(rdaXuLyAnh);

        bxY.add(rdaXuLyAnh);
        bxY.add(Box.createVerticalStrut(10));
        bxY.add(rdaTCA);
        pnl.add(bxY);
        bxWest.add(pnl);

        // --- Chọn phương pháp
        pnl = new JPanel();
        bxY = Box.createVerticalBox();
        pnl.setBorder(BorderFactory.createTitledBorder("Phương pháp chuyển đổi"));
        ButtonGroup btgPp = new ButtonGroup();
        rdaGamma = new JRadioButton("Gamma");
        rdaNega = new JRadioButton("Negative");
        rdaLog = new JRadioButton("Log");
        
        rdaGamma.addActionListener(this);
        rdaNega.addActionListener(this);
        rdaLog.addActionListener(this);

        btgPp.add(rdaGamma);
        btgPp.add(rdaNega);
        btgPp.add(rdaLog);

        bxY.add(rdaGamma);
        bxY.add(Box.createVerticalStrut(10));
        bxY.add(rdaNega);
        bxY.add(Box.createVerticalStrut(10));
        bxY.add(rdaLog);
        pnl.add(bxY);
        bxWest.add(pnl);

        // --- Chọn tác vụ
        pnl = new JPanel();
        bxY = Box.createVerticalBox();
        pnl.setBorder(BorderFactory.createTitledBorder("Chọn tác vụ"));
        btnChonAnh = new JButton("Chọn ảnh");
        btnThucHien = new JButton("Thực hiện");
        btnReset = new JButton("Reset");
        btnExit = new JButton("Exit");

        btnChonAnh.setMaximumSize(new Dimension(150, 80));
        btnThucHien.setMaximumSize(new Dimension(150, 80));
        btnReset.setMaximumSize(new Dimension(150, 80));
        btnExit.setMaximumSize(new Dimension(150, 80));
        
        btnChonAnh.addActionListener(this);
        btnThucHien.addActionListener(this);
        btnReset.addActionListener(this);
        btnExit.addActionListener(this);

        bxY.add(btnChonAnh);
        bxY.add(Box.createVerticalStrut(10));
        bxY.add(btnThucHien);
        bxY.add(Box.createVerticalStrut(10));
        bxY.add(btnReset);
        bxY.add(Box.createVerticalStrut(10));
        bxY.add(btnExit);
        pnl.add(bxY);
        bxWest.add(pnl);

        pnlWest.add(bxWest);
        add(pnlWest, BorderLayout.WEST);

        // --- Center: nơi hiển thị ảnh
        pnlCenter = new JPanel();
        pnlCenter.setBorder(BorderFactory.createTitledBorder("Hiện ảnh"));		
        lblImage = new JLabel();  
        pnlCenter.add(lblImage);
        add(pnlCenter, BorderLayout.CENTER);

        // --- South: đường dẫn + kết quả
        Box bxX = Box.createHorizontalBox();
        pnlSouth = new JPanel();
        pnlSouth.setPreferredSize(new Dimension(600, 130));
        pnlSouth.setBorder(BorderFactory.createTitledBorder(""));

        pnl = new JPanel();
        pnl.setBorder(BorderFactory.createTitledBorder("Biển số: "));
        pnl.setPreferredSize(new Dimension(600, 110));        
        lblImageRes = new JLabel("Kết quả");
        pnl.add(lblImageRes);
        bxX.add(pnl);
        bxX.add(Box.createHorizontalStrut(20));
        
        pnl = new JPanel();
        pnl.setBorder(BorderFactory.createTitledBorder("Đường link: "));
        pnl.setPreferredSize(new Dimension(300, 110));  
        lblPath = new JLabel("Chưa chọn ảnh");
        pnl.add(lblPath);
        bxX.add(pnl);

        pnlSouth.add(bxX);
        add(pnlSouth, BorderLayout.SOUTH);
    }

    public static void main(String[] args) {
        new MainGUI();
    }

    @SuppressWarnings("null")
	@Override
    public void actionPerformed(ActionEvent e) {
        try {
            Object source = e.getSource();
            if (source.equals(btnChonAnh)) {
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setDialogTitle("Chọn một ảnh");
                fileChooser.setFileFilter(new javax.swing.filechooser.FileNameExtensionFilter(
                        "Hình ảnh", "jpg", "png", "jpeg", "bmp", "gif"));

                int result = fileChooser.showOpenDialog(this);

                if (result == JFileChooser.APPROVE_OPTION) {
                    file = fileChooser.getSelectedFile();
                    lblPath.setText("Ảnh đã chọn: " + file.getAbsolutePath());

                    // Load ảnh vào lblImage
                    ImageIcon imageIcon = new ImageIcon(file.getAbsolutePath());
                    Image image = imageIcon.getImage();
                    Image scaledImage = image.getScaledInstance(600, 380, Image.SCALE_SMOOTH);
                    lblImage.setIcon(new ImageIcon(scaledImage));
                }
            } else if (source.equals(btnExit)) {
                System.exit(0);
            }else if (source.equals(btnReset)) {
                lblImage.setText("Trống");
                lblImageRes.setText("Kết quả");
                lblImage.setIcon(null);
                lblImageRes.setIcon(null);
                
                rdaGamma.setSelected(false);
                rdaNega.setSelected(false);
                rdaLog.setSelected(false);
                rdaTCA.setSelected(false);
                rdaXuLyAnh.setSelected(false);
            } else if (source.equals(btnThucHien)) {
            	if(rdaXuLyAnh.isSelected()) {
            		try {
                        if (file == null) {
                        	JOptionPane.showMessageDialog(this, "Vui lòng chọn ảnh trước!", "Error", JOptionPane.ERROR_MESSAGE);
                            return;
                        }

                        String inputImg = file.getAbsolutePath(); // ảnh người dùng chọn
                        String outputImg = "D:/2025-2026/IMAGE_PROCESSING/output_plate.jpg";

                        ProcessBuilder pb = new ProcessBuilder(
                            "python", "D:/2025-2026/IMAGE_PROCESSING/Project/src/scripts/nhan_dien_ban_so.py", inputImg, outputImg
                        );
                        Process process = pb.start();

                        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
                        String line;
                        while ((line = reader.readLine()) != null) {
                            System.out.println("Python: " + line);
                        }
                        
                        int exitCode = process.waitFor();
                        System.out.println("Python kết thúc với mã: " + exitCode);

                        // Load ảnh kết quả từ Python
                        ImageIcon icon = new ImageIcon(outputImg);
                        Image image = icon.getImage();
                        Image scaledImage = image.getScaledInstance(400, 80, Image.SCALE_SMOOTH);
                        lblImageRes.setText("");                      
                        lblImageRes.setIcon(new ImageIcon(scaledImage));

                    } catch (Exception ex) {
                        ex.printStackTrace();
                        lblResult.setText("Lỗi khi chạy Python!");
                        JOptionPane.showConfirmDialog(this, "Lỗi", "Error", JOptionPane.ERROR_MESSAGE);
                    }
            	}else if(rdaTCA.isSelected()) {
            		try {
            	        // Gọi script Python với đường dẫn ảnh
            	        ProcessBuilder pb = new ProcessBuilder(
            	            "python", "D:/2025-2026/IMAGE_PROCESSING/Project/src/scripts/cai_thien_anh.py", file.getAbsolutePath(), "output.png"
            	        );
            	        pb.redirectErrorStream(true);
            	        Process process = pb.start();

            	        // Đọc log từ Python
            	        BufferedReader reader = new BufferedReader(
            	            new InputStreamReader(process.getInputStream()));
            	        String line;
            	        while ((line = reader.readLine()) != null) {
            	            System.out.println("[PYTHON] " + line);
            	        }
            	        process.waitFor();

            	        ImageIcon icon = new ImageIcon("output.png");
            	        Image image = icon.getImage();
            	        Image scaledImage = image.getScaledInstance(600, 380, Image.SCALE_SMOOTH);
                        lblImage.setText("");                      
                        lblImage.setIcon(new ImageIcon(scaledImage));
                    } catch (Exception ex) {
                        ex.printStackTrace();
                        lblResult.setText("Lỗi khi chạy Python!");
                        JOptionPane.showConfirmDialog(this, "Lỗi", "Error", JOptionPane.ERROR_MESSAGE);
                    }
            	}else {
            		JOptionPane.showConfirmDialog(this, "Vui lòng chọn yêu cầu!", "Error", JOptionPane.ERROR_MESSAGE);
            	}
            }
        } catch (Exception e2) {
            e2.printStackTrace();
            JOptionPane.showConfirmDialog(this, "Lỗi", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
