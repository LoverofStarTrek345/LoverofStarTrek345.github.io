import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.ActionEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.text.DecimalFormat;
import javax.swing.AbstractAction;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.KeyStroke;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import javax.swing.Timer;

public class App {
    private static final double GRAVITY = 9.81; // m/s^2
    private static final double AIR_DENSITY = 1.225; // kg/m^3
    private static final double DRAG_COEFFICIENT = 1.0;
    private static final double FRONTAL_AREA = 0.5; // m^2
    private static final double ROLLING_RESISTANCE = 0.025;
    private static final double TIME_STEP = 0.02; // seconds

    private final DecimalFormat numberFormat = new DecimalFormat("0.00");
    private final JTextField massField = new JTextField("25", 6);
    private final JTextField motorField = new JTextField("120", 6);
    private final JTextField durationField = new JTextField("60", 6);
    private final JLabel statusLabel = new JLabel("Ready — press Start, then hold a direction.");
    private final JLabel massValue = new JLabel();
    private final JLabel weightValue = new JLabel();
    private final JLabel speedValue = new JLabel();
    private final JLabel positionValue = new JLabel();
    private final JLabel dragValue = new JLabel();
    private final JLabel timeValue = new JLabel();
    private final JButton startButton = new JButton("Start");
    private final RobotView robotView = new RobotView();
    private final Timer timer;

    private double mass = 25.0;
    private double motorForce = 120.0;
    private double duration = 60.0;
    private double elapsed;
    private double velocity;
    private double position;
    private double drag;
    private int throttle;
    private boolean running;

    private App() {
        timer = new Timer(20, event -> advance());
        buildWindow();
        updateTelemetry();
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new App().show());
    }

    private void show() {
        JFrame frame = new JFrame("Robot Physics Simulator");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(createContent());
        frame.pack();
        frame.setMinimumSize(new Dimension(760, 560));
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
        frame.getRootPane().setDefaultButton(startButton);
    }

    private void buildWindow() {
        startButton.addActionListener(event -> {
            if (running) {
                pause("Paused.");
            } else if (elapsed >= duration) {
                statusLabel.setText("Simulation finished — reset to run again.");
            } else {
                running = true;
                startButton.setText("Pause");
                statusLabel.setText("Running — hold Left/Right or use the controls.");
                timer.start();
                robotView.requestFocusInWindow();
            }
        });

        installThrottleControls();
    }

    private JPanel createContent() {
        JPanel root = new JPanel(new BorderLayout(12, 12));
        root.setBorder(BorderFactory.createEmptyBorder(16, 18, 14, 18));
        root.setBackground(new Color(244, 247, 251));

        JLabel title = new JLabel("ROBOT PHYSICS SIMULATOR");
        title.setFont(new Font("SansSerif", Font.BOLD, 20));
        title.setForeground(new Color(25, 42, 63));
        root.add(title, BorderLayout.NORTH);

        JPanel center = new JPanel(new BorderLayout(0, 10));
        center.setOpaque(false);
        robotView.setPreferredSize(new Dimension(800, 330));
        center.add(robotView, BorderLayout.CENTER);
        center.add(createTelemetryPanel(), BorderLayout.SOUTH);
        root.add(center, BorderLayout.CENTER);
        root.add(createControlPanel(), BorderLayout.EAST);

        statusLabel.setForeground(new Color(70, 88, 110));
        root.add(statusLabel, BorderLayout.SOUTH);
        return root;
    }

    private JPanel createControlPanel() {
        JPanel panel = new JPanel();
        panel.setLayout(new javax.swing.BoxLayout(panel, javax.swing.BoxLayout.Y_AXIS));
        panel.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(216, 225, 235)),
                BorderFactory.createEmptyBorder(14, 14, 14, 14)));
        panel.setBackground(Color.WHITE);

        JLabel heading = new JLabel("ROBOT SETUP");
        heading.setFont(new Font("SansSerif", Font.BOLD, 14));
        heading.setAlignmentX(Component.LEFT_ALIGNMENT);
        panel.add(heading);
        panel.add(new JLabel("Mass (kg)"));
        panel.add(massField);
        panel.add(new JLabel("Motor force (N)"));
        panel.add(motorField);
        panel.add(new JLabel("Duration (s)"));
        panel.add(durationField);
        panel.add(new JLabel(" "));

        startButton.setAlignmentX(Component.LEFT_ALIGNMENT);
        panel.add(startButton);
        JButton resetButton = new JButton("Reset");
        resetButton.setAlignmentX(Component.LEFT_ALIGNMENT);
        resetButton.addActionListener(event -> reset());
        panel.add(resetButton);
        panel.add(new JLabel(" "));
        panel.add(new JLabel("DRIVE"));
        panel.add(makeHoldButton("Forward  →", 1));
        panel.add(makeHoldButton("←  Reverse", -1));
        panel.add(new JLabel(" "));

        JLabel keys = new JLabel("<html>Keyboard controls:<br>← / → or A / D</html>");
        keys.setForeground(new Color(90, 105, 122));
        panel.add(keys);
        panel.add(new JLabel(" "));
        JLabel physics = new JLabel("<html><b>Physics constants</b><br>"
                + "Gravity: " + GRAVITY + " m/s²<br>"
                + "Air density: " + AIR_DENSITY + " kg/m³<br>"
                + "Drag coefficient: " + DRAG_COEFFICIENT + "<br>"
                + "Frontal area: " + FRONTAL_AREA + " m²<br>"
                + "Rolling resistance: " + ROLLING_RESISTANCE + "</html>");
        physics.setForeground(new Color(75, 91, 109));
        panel.add(physics);
        return panel;
    }

    private JPanel createTelemetryPanel() {
        JPanel panel = new JPanel(new java.awt.GridLayout(2, 3, 8, 4));
        panel.setBorder(BorderFactory.createEmptyBorder(5, 2, 2, 2));
        panel.setOpaque(false);
        addMetric(panel, "MASS", massValue);
        addMetric(panel, "WEIGHT", weightValue);
        addMetric(panel, "SPEED", speedValue);
        addMetric(panel, "POSITION", positionValue);
        addMetric(panel, "AIR DRAG", dragValue);
        addMetric(panel, "TIME", timeValue);
        return panel;
    }

    private void addMetric(JPanel panel, String name, JLabel value) {
        JPanel metric = new JPanel(new BorderLayout(0, 2));
        metric.setBackground(Color.WHITE);
        metric.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(225, 231, 238)),
                BorderFactory.createEmptyBorder(7, 9, 7, 9)));
        JLabel label = new JLabel(name);
        label.setFont(new Font("SansSerif", Font.BOLD, 10));
        label.setForeground(new Color(110, 125, 143));
        value.setFont(new Font("SansSerif", Font.BOLD, 16));
        value.setForeground(new Color(35, 57, 82));
        metric.add(label, BorderLayout.NORTH);
        metric.add(value, BorderLayout.CENTER);
        panel.add(metric);
    }

    private JButton makeHoldButton(String text, int direction) {
        JButton button = new JButton(text);
        button.setAlignmentX(Component.LEFT_ALIGNMENT);
        button.addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent event) {
                setThrottle(direction);
            }

            @Override
            public void mouseReleased(MouseEvent event) {
                if (throttle == direction) {
                    setThrottle(0);
                }
            }

            @Override
            public void mouseExited(MouseEvent event) {
                if ((event.getModifiersEx() & MouseEvent.BUTTON1_DOWN_MASK) == 0
                        && throttle == direction) {
                    setThrottle(0);
                }
            }
        });
        return button;
    }

    private void installThrottleControls() {
        bindThrottle(KeyStroke.getKeyStroke("pressed RIGHT"), "rightPressed", 1);
        bindThrottle(KeyStroke.getKeyStroke("released RIGHT"), "rightReleased", 0);
        bindThrottle(KeyStroke.getKeyStroke("pressed D"), "dPressed", 1);
        bindThrottle(KeyStroke.getKeyStroke("released D"), "dReleased", 0);
        bindThrottle(KeyStroke.getKeyStroke("pressed LEFT"), "leftPressed", -1);
        bindThrottle(KeyStroke.getKeyStroke("released LEFT"), "leftReleased", 0);
        bindThrottle(KeyStroke.getKeyStroke("pressed A"), "aPressed", -1);
        bindThrottle(KeyStroke.getKeyStroke("released A"), "aReleased", 0);
    }

    private void bindThrottle(KeyStroke key, String name, int direction) {
        robotView.getInputMap(JPanel.WHEN_IN_FOCUSED_WINDOW).put(key, name);
        robotView.getActionMap().put(name, new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent event) {
                setThrottle(direction);
            }
        });
    }

    private void setThrottle(int direction) {
        throttle = direction;
        robotView.repaint();
    }

    private void advance() {
        if (!running) {
            return;
        }
        double step = Math.min(TIME_STEP, duration - elapsed);
        double driveForce = throttle * motorForce;
        double dragForce = 0.5 * AIR_DENSITY * DRAG_COEFFICIENT
                * FRONTAL_AREA * velocity * Math.abs(velocity);
        double rollingForce = velocity == 0.0 ? 0.0
                : Math.copySign(ROLLING_RESISTANCE * mass * GRAVITY, velocity);
        double netForce = driveForce - dragForce - rollingForce;

        if (velocity == 0.0 && throttle == 0) {
            netForce = 0.0;
        } else if (velocity != 0.0 && Math.signum(netForce) != Math.signum(velocity)
                && Math.abs(netForce) <= Math.abs(dragForce + rollingForce)) {
            netForce = 0.0;
        }

        velocity += netForce / mass * step;
        if (Math.abs(velocity) < 0.005 && throttle == 0) {
            velocity = 0.0;
        }
        position = Math.max(0.0, position + velocity * step);
        if (position == 0.0 && velocity < 0.0) {
            velocity = 0.0;
        }
        elapsed += step;
        drag = 0.5 * AIR_DENSITY * DRAG_COEFFICIENT * FRONTAL_AREA
                * velocity * Math.abs(velocity);
        updateTelemetry();
        robotView.repaint();

        if (elapsed >= duration) {
            pause("Simulation complete — reset to run again.");
        }
    }

    private void pause(String message) {
        running = false;
        throttle = 0;
        timer.stop();
        startButton.setText("Start");
        statusLabel.setText(message);
        robotView.repaint();
    }

    private void reset() {
        try {
            double newMass = parsePositive(massField, "Mass");
            double newMotorForce = parsePositive(motorField, "Motor force");
            double newDuration = parsePositive(durationField, "Duration");
            mass = newMass;
            motorForce = newMotorForce;
            duration = newDuration;
        } catch (IllegalArgumentException exception) {
            statusLabel.setText(exception.getMessage());
            return;
        }

        running = false;
        timer.stop();
        throttle = 0;
        elapsed = 0.0;
        velocity = 0.0;
        position = 0.0;
        drag = 0.0;
        startButton.setText("Start");
        statusLabel.setText("Reset — press Start, then hold a direction.");
        updateTelemetry();
        robotView.repaint();
    }

    private double parsePositive(JTextField field, String name) {
        try {
            double value = Double.parseDouble(field.getText().trim());
            if (Double.isFinite(value) && value > 0.0) {
                return value;
            }
        } catch (NumberFormatException ignored) {
            // Report invalid user input in the status bar below.
        }
        throw new IllegalArgumentException(name + " must be a number greater than zero.");
    }

    private void updateTelemetry() {
        massValue.setText(numberFormat.format(mass) + " kg");
        weightValue.setText(numberFormat.format(mass * GRAVITY) + " N");
        speedValue.setText(numberFormat.format(velocity) + " m/s");
        positionValue.setText(numberFormat.format(position) + " m");
        dragValue.setText(numberFormat.format(drag) + " N");
        timeValue.setText(numberFormat.format(elapsed) + " / " + numberFormat.format(duration) + " s");
    }

    private final class RobotView extends JPanel {
        private RobotView() {
            setBackground(new Color(225, 238, 248));
            setBorder(BorderFactory.createLineBorder(new Color(210, 222, 234)));
            setFocusable(true);
        }

        @Override
        protected void paintComponent(Graphics graphics) {
            super.paintComponent(graphics);
            Graphics2D g = (Graphics2D) graphics.create();
            g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

            int width = getWidth();
            int height = getHeight();
            int groundY = height - 54;
            g.setColor(new Color(238, 245, 249));
            g.fillRect(0, 0, width, groundY);
            g.setColor(new Color(169, 190, 204));
            g.fillRect(0, groundY, width, height - groundY);
            g.setColor(new Color(136, 161, 178));
            g.setStroke(new BasicStroke(2));
            g.drawLine(0, groundY, width, groundY);

            double metersPerMark = 2.0;
            int spacing = 80;
            double offset = (position % metersPerMark) / metersPerMark * spacing;
            g.setFont(new Font("SansSerif", Font.PLAIN, 11));
            for (int x = (int) -offset; x < width; x += spacing) {
                g.setColor(new Color(151, 173, 188));
                g.drawLine(x, groundY + 2, x, groundY + 12);
                double marker = Math.floor(position / metersPerMark) * metersPerMark
                        + (x + offset) / spacing * metersPerMark;
                g.drawString(numberFormat.format(Math.max(0.0, marker)) + " m", x + 3, groundY + 28);
            }

            int robotX = Math.max(40, (int) (width * 0.43));
            int robotY = groundY - 82;
            g.setColor(new Color(55, 83, 111, 45));
            g.fillOval(robotX - 5, groundY - 4, 122, 12);

            g.setColor(new Color(38, 60, 82));
            g.fillRoundRect(robotX + 9, robotY + 52, 24, 25, 8, 8);
            g.fillRoundRect(robotX + 79, robotY + 52, 24, 25, 8, 8);
            g.setColor(new Color(48, 65, 79));
            g.fillOval(robotX + 10, robotY + 68, 23, 23);
            g.fillOval(robotX + 80, robotY + 68, 23, 23);
            g.setColor(new Color(192, 207, 218));
            g.fillOval(robotX + 17, robotY + 75, 9, 9);
            g.fillOval(robotX + 87, robotY + 75, 9, 9);

            g.setColor(new Color(38, 137, 187));
            g.fillRoundRect(robotX, robotY + 15, 112, 50, 13, 13);
            g.setColor(new Color(33, 100, 145));
            g.fillRoundRect(robotX + 15, robotY, 65, 37, 12, 12);
            g.setColor(new Color(197, 235, 246));
            g.fillRoundRect(robotX + 26, robotY + 8, 41, 21, 7, 7);
            g.setColor(new Color(27, 57, 78));
            g.fillOval(robotX + 38, robotY + 14, 7, 7);
            g.fillOval(robotX + 52, robotY + 14, 7, 7);
            g.setColor(Color.WHITE);
            g.setFont(new Font("SansSerif", Font.BOLD, 11));
            g.drawString("BOT", robotX + 43, robotY + 53);

            if (running && throttle != 0) {
                g.setColor(throttle > 0 ? new Color(240, 145, 63) : new Color(107, 155, 224));
                int flameX = throttle > 0 ? robotX - 18 : robotX + 112;
                int[] flameXs = throttle > 0
                        ? new int[] {robotX + 1, robotX - 18, robotX + 1}
                        : new int[] {robotX + 111, robotX + 130, robotX + 111};
                int[] flameYs = {robotY + 39, robotY + 47, robotY + 55};
                g.fillPolygon(flameXs, flameYs, 3);
                g.setColor(new Color(50, 67, 84));
                g.drawString(throttle > 0 ? "FORWARD THRUST" : "REVERSE THRUST",
                        flameX - 6, robotY - 12);
            } else {
                g.setColor(new Color(83, 105, 125));
                g.setFont(new Font("SansSerif", Font.BOLD, 13));
                g.drawString("Hold a direction to drive", 18, 28);
            }

            g.setColor(new Color(67, 88, 109));
            g.setFont(new Font("SansSerif", Font.PLAIN, 12));
            g.drawString("Position: " + numberFormat.format(position) + " m", 18, height - 9);
            g.dispose();
        }
    }
}
